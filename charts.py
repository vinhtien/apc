# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 22:16:25 2017

@author: jswim
"""
import numpy as np
import Extraction
from bokeh.plotting import figure, show


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
        graph = figure(title='Frequency of Posts Per Year', x_axis_label='Posts', y_axis_label='Year')
        graph.line(self.yearrange, yearbins, legend='Posts', line_width=2)
        return graph
        
        
    def getPostsPerMonthLine(self):
        monthbins = [list(self.months).count(self.monthrange[i]) for i in range(len(self.monthrange))]
        graph = figure(title='Frequency of Posts per Month', x_axis_label='Month', y_axis_label='Posts')
        graph.line(self.monthrange, monthbins, legend='Posts', line_width=2)
        return graph
    
    def getPostsPerDayOfWeekLine(self):
        daybins = [list(self.days).count(self.dayrange[i]) for i in range(len(self.dayrange))]
        graph = figure(title='Frequency of Posts per Day', x_axis_label='Day', y_axis_label='Posts')
        graph.line(self.dayrange, daybins, legend='Posts', line_width=2)
        return graph

    def getPostsPerHourLine(self):
        hourbins = [list(self.hours).count(self.hourrange[i]) for i in range(len(self.hourrange))]
        graph = figure(title='Frequency of Posts per Hour', x_axis_label='Hour', y_axis_label='Posts')
        graph.line(self.hourrange, hourbins, legend = 'Posts', line_width=2)
        return graph
    
    def getReactsPerPostHourBars(self):
        df = self.data.getTimeSeriesIndexDFAll()['reactions'].groupby(self.hours)
        hourbins = [len(df.get_group(i)) for i in range(len(self.hourrange))]
        graph = figure(title = 'Reactions per Post Hour', x_axis_label='Hour', y_axis_label='Reactions')
        graph.vbar(self.hourrange, top=hourbins, width = 0.5)
        return graph



'''
friendrange = [i[0] for i in typereact]
dffriendreacts = dfreacts['name']



def getFriendsNReactPie():
    reactbins = [list(dfreacts['name']).count(friendrange[i]) for i in range(len(friendrange))]
    explode = [0.5 for i in range(len(friendrange))]
    fig1, ax1 = plt.subplots()
    ax1.pie(reactbins, explode=explode, labels=friendrange, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')
    plt.show()

'''
c = ChartLauncher()
#c.getPostsPerYearLine()
#c.getPostsPerMonthLine()
#c.getPostsPerDayOfWeekLine()
#c.getPostsPerHourLine()
#c.getReactsPerPostHourBars()
#df = c.data.getTimeSeriesIndexDFAll()
