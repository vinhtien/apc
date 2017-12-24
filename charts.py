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


class ChartLauncher:
    def __init__(self):
        self.data = Extraction.Extraction()
        self.time = self.data.time
        self.years = self.time.year
        self.yearrange = list(map(int, sorted(set(sorted(self.years)[1:]))))
        self.months = self.time.month
        self.monthrange = np.arange(1, 13)
        self.days = self.time.dayofweek
        self.dayrange = np.arange(7)
        self.hours = self.time.hour
        self.hourrange = np.arange(24)

    def getPostsPerYearLine(self):
        yearbins = [list(self.years).count(self.yearrange[i]) for i in range(len(self.yearrange))]
        l = LineGraph(yearrange, yearbins, 'Year', 'Posts', ' Frequency of Posts Posts Per Year', 'Posts', 'ppyl.html')
        l.spawnLineGraph()

    def getPostsPerMonthLine(self):
        monthbins = [list(self.months).count(self.monthrange[i]) for i in range(len(self.monthrange))]
        l = LineGraph(self.monthrange, monthbins, 'Month', 'Posts', 'Frequency of Posts per Month', 'Posts',
                      'ppml.html')
        l.spawnLineGraph()

    def getPostsPerDayOfWeekLine(self):
        daybins = [list(self.days).count(self.dayrange[i]) for i in range(len(self.dayrange))]
        l = LineGraph(self.dayrange, daybins, 'Day', 'Posts', 'Frequency of Posts per Day', 'Posts', 'ppdl.html')
        l.spawnLineGraph()

    def getPostsPerHourLine(self):
        hourbins = [list(self.hours).count(self.hourrange[i]) for i in range(len(self.hourrange))]
        l = LineGraph(self.hourrange, hourbins, 'Hour', 'Posts', 'Frequency of Posts per Hour', 'Posts', 'pphl.html')
        l.spawnLineGraph()


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
        l.line(x, y, legend="Posts", line_width=2)
        show(l)


'''
###Reactions
# dfreacts = {'id':[i.get('id') for i in indextimereacts]}
# pd.DataFrame( columns=
###Getting ranges, making bins and splitting up data


dfreacts = [i for nest in reacts for i in nest]
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


def getFriendsNReactPie():
    reactbins = [list(dfreacts['name']).count(friendrange[i]) for i in range(len(friendrange))]
    explode = [0.5 for i in range(len(friendrange))]
    fig1, ax1 = plt.subplots()
    ax1.pie(reactbins, explode=explode, labels=friendrange, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')
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

'''
# c = ChartLauncher()
# c.getPostsPerHourLine()
