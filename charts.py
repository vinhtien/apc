import numpy as np
import Extraction
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
from bokeh.embed import components


class ChartLauncher:
    '''
    ChartLauncher() take output from Extraction() and has methods to launch individual charts.
    '''
    def __init__(self, output):
        self.data = Extraction.Extraction(output)
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
        '''
        Returns a line graph which has your number of posts on y-axis and years on x-axis.
        '''
        yearbins = [list(self.years).count(self.yearrange[i]) for i in range(len(self.yearrange))]
        graph = figure(title='Frequency of Posts Per Year', x_axis_label='Posts', y_axis_label='Year')
        graph.line(self.yearrange, yearbins, legend='Posts', line_width=2)
        graph.toolbar_location="above"
        return graph
        
        
    def getPostsPerMonthLine(self):
        '''
        Returns a line graph which has your number of posts on y-axis and months on x-axis.
        '''
        monthbins = [list(self.months).count(self.monthrange[i]) for i in range(len(self.monthrange))]
        graph = figure(title='Frequency of Posts per Month', x_axis_label='Month', y_axis_label='Posts')
        graph.line(self.monthrange, monthbins, legend='Posts', line_width=2)
        graph.toolbar_location="above"
        return graph
    
    def getPostsPerDayOfWeekLine(self):
        '''
        Returns a line graph which has your number of posts on y-axis and days of week on x-axis.
        '''
        daybins = [list(self.days).count(self.dayrange[i]) for i in range(len(self.dayrange))]
        graph = figure(title='Frequency of Posts per Day', x_axis_label='Day', y_axis_label='Posts')
        graph.line(self.dayrange, daybins, legend='Posts', line_width=2)
        graph.toolbar_location="above"
        return graph

    def getPostsPerHourLine(self):
        '''
        Returns a line graph which has your number of posts on y-axis and hour on x-axis.
        '''
        hourbins = [list(self.hours).count(self.hourrange[i]) for i in range(len(self.hourrange))]
        graph = figure(title='Frequency of Posts per Hour', x_axis_label='Hour', y_axis_label='Posts')
        graph.line(self.hourrange, hourbins, legend = 'Posts', line_width=2)
        graph.toolbar_location="above"
        return graph
    
    def getReactsPerPostHourBars(self):
        '''
        Returns a vertical bar graph which has number of reactions per post/hour on y-axis and hours on x-axis.
        '''
        df, hourbins = [], []
        try:
            df = self.data.getTimeSeriesIndexDFAll()['reactions'].groupby(self.hours)
            hourbins = [len(df.get_group(i)) for i in range(len(self.hourrange))]
        except KeyError: # no reactions found
            pass
        graph = figure(title = 'Reactions per Post Hour', x_axis_label='Hour', y_axis_label='Reactions')
        graph.vbar(self.hourrange, top=hourbins, width = 0.5)
        graph.toolbar_location="above"
        return graph
    
    def getFriendsNReactBars(self):
        '''
        Doesn't work because can't figure out how to display so many names. 
        '''
        df = self.data.getNumTypeReactionsDF().groupby('name')
        keys = list(df.groups.keys())
        colors = ['#f44242', '#d6f441', '#8e41f4', '#4641f4', '#43f441', '#f4a641']
        legend = ['angry', 'haha', 'like', 'love', 'sad', 'wow']
        data = {'friends':keys,
                'angry':[df.get_group(i)['ANGRY'][0] for i in keys],
                'haha':[df.get_group(i)['HAHA'][0] for i in keys],
                'like':[df.get_group(i)['LIKE'][0] for i in keys],
                'love':[df.get_group(i)['LOVE'][0] for i in keys],
                'sad':[df.get_group(i)['SAD'][0] for i in keys],
                'wow':[df.get_group(i)['WOW'][0] for i in keys]}
        source = ColumnDataSource(data=data)
        
        graph = figure(x_range=keys, title='Reactions per Friend', width=1000)
        graph.vbar_stack(legend, x= 'friends' , width=1, color=colors, source=source, legend=legend)
        graph.y_range.start = 0
        graph.x_range.range_padding = 0.5
        graph.legend.location = 'top_right'
        graph.legend.orientation = 'horizontal'
        #show(graph)
        return graph
        

    def getAllComponents(self):
        """ returns all charts as a list of components """
        return ([components(self.getPostsPerYearLine()),
                components(self.getPostsPerMonthLine()),
                components(self.getPostsPerDayOfWeekLine()),
                components(self.getPostsPerHourLine()),
                components(self.getReactsPerPostHourBars())])


