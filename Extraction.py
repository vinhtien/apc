# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 14:52:36 2017

@author: jswim
"""
import json
import pandas as pd
import numpy as np
import collections

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
        typereact = list(dfreacts.groupby('name')['type'])
        reactrange = list(dfreacts.groupby('type'))
        reactrange = [reactrange[i][0] for i in range(len(reactrange))]
        friendrange = [i[0] for i in typereact]
        # ntypereacts makes per friend a list of count per reaction type
        ntypereacts = [[list(list(typereact)[i][1]).count(reactrange[j]) for j in range(len(reactrange))] for i in
                       range(len(friendrange))]
        frcolumns = ['name', 'ANGRY', 'HAHA', 'LIKE', 'LOVE', 'SAD', 'WOW', 'total']
        dfdict = {'name': friendrange,
                  'ANGRY': [i[0] for i in ntypereacts],
                  'HAHA': [i[1] for i in ntypereacts],
                  'LIKE': [i[2] for i in ntypereacts],
                  'LOVE': [i[3] for i in ntypereacts],
                  'SAD': [i[4] for i in ntypereacts],
                  'WOW': [i[5] for i in ntypereacts],
                  'total': [list(dfreacts['name']).count(friendrange[i]) for i in range(len(friendrange))]}
        return pd.DataFrame(dfdict, columns=frcolumns).set_index('name')

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
                    names.append(flat.get('from').get('name'))
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