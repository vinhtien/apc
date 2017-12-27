import json
import pandas as pd
import numpy as np

file = open('postsNreactz.txt', 'r')
output = json.loads(file.read())


class Extraction:
    '''
    Extraction() makes pandas.DataFrames of json output.
    Columns=['comments', 'id', 'message', 'reactions', 'stories', 'created_time']
    Converts timestamps to datetime objects.
    '''

    def __init__(self):
        self._df = pd.DataFrame({
            'comments': [i.get('comments') for i in output],
            'id': [i.get('id') for i in output],
            'message': [i.get('message') for i in output],
            'reactions': [i.get('reactions') for i in output],
            'stories': [i.get('story') for i in output],
            'created_time': [i.get('created_time') for i in output]},
            columns=['comments',
                     'id',
                     'message',
                     'reactions',
                     'stories',
                     'created_time'])
        self.time = pd.DatetimeIndex(self._df.created_time)

    def getTimeSeriesIndexDFAll(self):
        '''
        Returns pandas.DataFrame() with index of time.
        '''
        return self._df.set_index('created_time')

    def getReactionsDFAll(self):
        '''
        Flattens list of list of dictionaries into List of diciontaries.
        Returns pandas.DataFrame() with columns=['id', 'name', 'type']

        '''
        dfreacts = [i for nest in self._df.reactions for i in nest]
        dfreacts = pd.DataFrame({'id': [i.get('id') for i in dfreacts],
                                 'name': [i.get('name') for i in dfreacts],
                                 'type': [i.get('type') for i in dfreacts]},
                                columns=['id', 'name', 'type'])
        return dfreacts

    def getNumTypeReactionsDF(self):
        '''
        Returns a pandas.DataFrame() with columns = ['name','ANGRY', 'HAHA', 'LIKE', 'LOVE', 'SAD', 'WOW','total']
        '''
        dfreacts = self.getReactionsDFAll()
        typereact = dfreacts.groupby('name')
        friendrange = list(typereact.groups.keys())
        angry, haha, like, love, sad, wow = [], [], [], [], [], []

        for i in friendrange:
            try:
                react = typereact.get_group(i).groupby('type').get_group('ANGRY')
                angry.append(react.shape[0])
            except:
                angry.append(0)
            try:
                react = typereact.get_group(i).groupby('type').get_group('HAHA')
                haha.append(react.shape[0])
            except:
                haha.append(0)
            try:
                react = typereact.get_group(i).groupby('type').get_group('LIKE')
                like.append(react.shape[0])
            except:
                like.append(0)
            try:
                react = typereact.get_group(i).groupby('type').get_group('LOVE')
                love.append(react.shape[0])
            except:
                love.append(0)
            try:
                react = typereact.get_group(i).groupby('type').get_group('SAD')
                sad.append(react.shape[0])
            except:
                sad.append(0)
            try:
                react = typereact.get_group(i).groupby('type').get_group('WOW')
                wow.append(react.shape[0])
            except:
                wow.append(0)

        frcolumns = ['name', 'ANGRY', 'HAHA', 'LIKE', 'LOVE', 'SAD', 'WOW']
        dfdict = {'name':friendrange, 'ANGRY':angry, 'HAHA':haha, 'LIKE':like, 'LOVE':love, 'SAD':sad, 'WOW':wow}
        df = pd.DataFrame(dfdict, columns=frcolumns)
        df['total'] = df.sum(axis=1)
        return df.set_index('name')

    def getnReactionsxFriendPivot(self):
        '''
        Returns a pandas.pivot_table() with index rows of all friends and columns of int [ANGRY', 'HAHA', 'LIKE', 'LOVE', 'SAD', 'WOW','total']
        '''
        pivot = pd.pivot_table(self.getNumTypeReactionsDF(), index='name')
        return pivot

    def getPostCommentMultiIndexDF(self):
        '''
        Returns a pandas.DataFrame() with MultiIndex() 'post_time':'comment_times':'name','message','delta'.

        '''
        comments = pd.DataFrame(self._df['comments'])
        indextups = []
        commtot = []
        nametot = []
        messagetot = []
        timedeltatot = []
        for i in range(len(comments)):
            if len(comments.iloc[i]) != 0:
                splay = comments.iloc[i][0]
                commtimes = []
                names = []
                messages = []
                timedeltas = []
                for j in range(len(splay)):
                    flat = splay[j]
                    ct = pd.to_datetime(flat.get('created_time'))
                    timedeltas.append(ct - self.time[i])
                    commtimes.append(ct)
                    try:
                        names.append(flat.get('from').get('name'))
                    except:
                        names.append('Others')
                    messages.append(flat.get('message'))

                indextups.extend([(self.time[i], commtimes[k]) for k in range(len(commtimes))])

                commtot.extend(commtimes)
                nametot.extend(names)
                messagetot.extend(messages)
                timedeltatot.extend(timedeltas)
            else:
                indextups.extend([(self.time[i], np.nan)])

        indexpc = pd.MultiIndex.from_tuples(indextups, names=('post_time', 'comment_time'))
        commentdf = pd.DataFrame({'name': nametot,
                                  'message': messagetot,
                                  'delta': timedeltatot}, index=indexpc)

        return commentdf

    def getFriendsCommentReactTotalDF(self, showCommentors=False):
        '''
        Returns pandas.DataFrame() with total number of comment and reaction for each friend. If there is
        no value for a particular column fills with 0. If showCommentors = False, 'name' is not returned in df
        as column. 
        '''
        commfriends = self.getPostCommentMultiIndexDF().groupby('name')
        ckeys = list(commfriends.groups.keys())
        reactfriends = self.getnReactionsxFriendPivot().groupby('name')
        rkeys = list(reactfriends.groups.keys())
        friendrange = list(set(ckeys + rkeys))
        reactots = []
        commtots = []
        for i in friendrange:
            if i in ckeys:
                commtots.append(len(commfriends.get_group(i)['name']))
            else:
                commtots.append(0)
            if i in rkeys:
                reactots.append(reactfriends.get_group(i)['total'][0])
            else:
                reactots.append(0)
        if(showCommentors): dfdict = {'name':friendrange, 'comments':commtots, 'reactions':reactots}
        else: dfdict = {'comments':commtots, 'reactions':reactots}
        df = pd.DataFrame(dfdict)
        return df
