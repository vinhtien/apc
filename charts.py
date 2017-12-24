# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 22:16:25 2017

@author: jswim
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import Extraction
import bokeh
from bokeh.plotting import figure, output_file, show

###Further extraction
data = Extraction.Extraction()._df

class LineGraph:
    def __init__(self, x, y, xlabel, ylabel, title, legend, outputfile):
        self._x = x
        self._y = y
        self._xlabel = xlabel
        self._ylabel = ylabel
        self._title = title
        self._legend = legend
        self._outputfile = outputfile

    def spawnLineGraph(self):
        x = self._x
        y = self._y
        l = figure(title=self._title, x_axis_label=self._xlabel, y_axis_label=self._ylabel)
        l.line(x, y, legend = "Posts", line_width=2)
        show(l)

times = pd.DatetimeIndex(data.created_time)
data = data.set_index('created_time')
###Reactions
# dfreacts = {'id':[i.get('id') for i in indextimereacts]}
# pd.DataFrame( columns=
###Getting ranges, making bins and splitting up data
reacts = data.reactions

dfreacts = [i for nest in reacts for i in nest]
print(dfreacts)
dfreacts = pd.DataFrame({'id': [i.get('id') for i in dfreacts],
                         'name': [i.get('name') for i in dfreacts],
                         'type': [i.get('type') for i in dfreacts]}, columns=['id', 'name', 'type'])
typereact = list(dfreacts.groupby('name')['type'])
reactrange = list(dfreacts.groupby('type'))
reactrange = [reactrange[i][0] for i in range(len(reactrange))]
friendrange = [i[0] for i in typereact]
dffriendreacts = dfreacts['name']
# for i in friendrange:


###
reactsyear = reacts.groupby(times.year)
databyyear = data.groupby(times.year)
years = times.year
yearrange = list(map(int, sorted(set(sorted(years)[1:]))))  # range-birthyear
###
reactsmonth = reacts.groupby(times.month)
databymonth = data.groupby(times.month)
months = times.month
monthrange = np.arange(13)
###
reactsday = reacts.groupby(times.dayofweek)
databydayofweek = data.groupby(times.dayofweek)
daysofweek = times.dayofweek
dayrange = np.arange(7)
###
reactshour = reacts.groupby(times.hour)
databyhour = data.groupby(times.hour)
hours = times.hour
hourrange = np.arange(24)



#Trying out pivot table
#dfreacts.pivot_table('', rows='title',
#                               cols='gender', aggfunc='mean')

def getFriendsNReactPie():
    reactbins = [list(dfreacts['name']).count(friendrange[i]) for i in range(len(friendrange))]
    explode = [0.5 for i in range(len(friendrange))]
    fig1, ax1 = plt.subplots()
    ax1.pie(reactbins, explode=explode, labels=friendrange, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')
    plt.show()


def getPostsPerYearLine():
    yearbins = [list(years).count(yearrange[i]) for i in range(len(yearrange))]
    l = LineGraph(yearrange, yearbins, 'Year', 'Posts', ' Frequency of Posts Posts Per Year', 'Posts', 'ppyl.html')
    l.spawnLineGraph()



def getPostsPerMonthLine():
    monthbins = [list(months).count(monthrange[i]) for i in range(len(monthrange))]
    plt.plot(monthrange, monthbins, label='Posts')
    # plt.plot(x2, y2, label ='Second Line')
    plt.xlabel('Month')
    plt.ylabel('Posts')
    plt.title('Frequency of posts per month')
    plt.xticks(np.arange(min(monthrange), max(monthrange) + 1, 1.0))
    plt.legend()
    plt.show()


def getPostsPerDayOfWeekLine():
    daybins = [list(daysofweek).count(dayrange[i]) for i in range(len(dayrange))]
    plt.plot(dayrange, daybins, label='Posts')
    # plt.plot(x2, y2, label ='Second Line')
    plt.xlabel('Day')
    plt.ylabel('Posts')
    plt.title('Frequency of posts per day')
    plt.xticks(np.arange(min(dayrange), max(dayrange) + 1, 1.0))
    plt.legend()
    plt.show()


def getPostsPerHourLine():
    hourbins = [list(hours).count(hourrange[i]) for i in range(len(hourrange))]
    plt.plot(hourrange, hourbins, label='Posts')
    plt.xlabel('Hour')
    plt.ylabel('Posts')
    plt.title('Frequency of your posts per hour')
    plt.xticks(np.arange(min(hourrange), max(hourrange) + 1, 1.0))
    plt.legend()
    plt.show()


def getPostsPerHourBars():
    hourbins = [list(hours).count(hourrange[i]) for i in range(len(hourrange))]
    plt.bar(hourrange, hourbins)
    plt.xlabel('Hour')
    plt.ylabel('Posts')
    plt.title('Frequency of your posts per hour')
    plt.xticks(np.arange(min(hourrange), max(hourrange) + 1, 1.0))
    plt.show()


# do more reacts/time
def getReactsPerHourBars():
    hourbins = [len(reactshour.get_group(i)) for i in range(len(hourrange))]
    plt.bar(hourrange, hourbins)
    plt.xlabel('Hour')
    plt.ylabel('Reactions')
    plt.title('Frequency of reactions per hour')
    plt.xticks(np.arange(min(hourrange), max(hourrange) + 1, 1.0))
    plt.show()


def getTypeReactsAll():
    reactbins = [len()]


l = LineGraph()

getPostsPerYearLine()

'''
plt.xlabel('Time')
plt.ylabel('Frequency')
plt.title('Frequency of posts during the day\n')
'''
