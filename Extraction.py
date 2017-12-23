# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 14:52:36 2017

@author: jswim
"""
import json
import pandas as pd
from Main import Main
#file = open('postsNreactz.txt', 'r')
#output = json.loads(file.read())

userToken = 'EAABZCTyXOsswBAApxn0ARmNZCLphvtgK63E6a4egOIKlxE6EFNbZBRZCmeZAmz0ug6iJNtO2U7DQ0lJJyhunCXNRAzaDYP3EPgoDFMgPxV5SaeswZB5DfsOZAHSyBrjhKID3AXjSM93Y89c7ZCYHSZBMfcLD5uKB6PWWGcpNdZChXRB5Tl7zTRWOyFcCVv49V6MHYZD'
userID = '545838748863640'
dataPath = 'D:\STUDY\MSCCOMPSCI\Proj_APC17\spa'
# if dataPath = NONE => it's fine, FileIO will use the same path of it
m = Main(userToken, userID, dataPath)

output = m.loadAllData()
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
        self._time = pd.DatetimeIndex(self._df.created_time)

    def getReactionsDFAll(self):
        '''
        Flattens list of list of dictionaries into List of Diciontaries.
        Returns pandas.DataFrame() with columns=['id', 'name', 'type']

        '''
        dfreacts = [i for nest in self._df.reactions for i in nest]
        dfreacts = pd.DataFrame({'id': [i.get('id') for i in dfreacts],
                                 'name': [i.get('name') for i in dfreacts],
                                 'type': [i.get('type') for i in dfreacts]},
                                columns=['id', 'name', 'type'])
        return dfreacts

    def getTimeSeriesIndexDFAll(self):
        '''
        Returns pandas.DataFrame() with
        '''
        return self._df.set_index('created_time')

    def getNumTypeReactionsDF(self):
        '''
        Returns a pandas.DataFrame()
        '''
        dfreacts = self.getReactionsDFAll()
        #print(dfreacts)
        typereact = list(dfreacts.groupby('name')['type'])
        #print(typereact)
        reactrange = list(dfreacts.groupby('type'))
        #print(reactrange)
        reactrange = [reactrange[i][0] for i in range(len(reactrange))]
        friendrange = [i[0] for i in typereact]
        # ntypereacts makes per friend a list of count per reaction type
        ntypereacts = [[list(list(typereact)[i][1]).count(reactrange[j]) for j in range(len(reactrange))] for i in
                       range(len(friendrange))]
        #print(ntypereacts)
        return
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
        Returns a pandas.pivot_table() with for rows of all friends and columns of
        '''
        pivot = pd.pivot_table(self.getNumTypeReactionsDF(), index='name', aggfunc='mean')
        return pivot


e = Extraction()
datetimedf = e.getTimeSeriesIndexDFAll()
nreactionxfriend = e.getNumTypeReactionsDF()
