import sys
sys.ps1 = 'SOMETHING'
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import datetime
from time import sleep
from random import randint

class fitbit_plotter():
    def __init__(self, user_data=None):
    #Expect user data in form: {'uid': {'dates': [date data], date2,...], steps:
    #       [step data]} '''
        plt.style.use('ggplot')
        plt.ion()
        self.fig = plt.figure()
        self.axes = plt.subplot(111)
        self.lines = []
        if user_data is None:
            user_data = {'1': {'dates': np.array(np.datetime64()),
                               'steps': np.array(np.nan)},
                         '2': {'dates': np.array(np.datetime64()),
                               'steps': np.array(np.nan)}}
        self.user_ids = user_data.keys()
        self.lines.append(self.axes.plot([np.datetime64(x) for x in
                                            user_data[self.user_ids[0]]['dates']],
                                          np.array(user_data[self.user_ids[0]]['steps']),
                                          color='r',
                                          label='User ' + self.user_ids[0]
                                         )[0])
        self.lines.append(self.axes.plot([np.datetime64(x) for x in
                                            user_data[self.user_ids[1]]['dates']],
                                          np.array(user_data[self.user_ids[1]]['steps']),
                                          color='b',
                                          label='User ' + self.user_ids[1]
                                         )[0])
        plt.legend()
        locator = mdates.DayLocator()
        formatter = mdates.DateFormatter('%m/%d')
        self.axes.xaxis.set_major_locator(locator)
        self.axes.xaxis.set_major_formatter(formatter)
        self.fig.autofmt_xdate()
        self.fig.canvas.draw()
        plt.show(block=False)

    def add_data(self, user_data):
        plt.ion()
        for user_id in user_data.keys():
            idx = self.user_ids.index(user_id)
            dates_to_add = np.array([np.datetime64(x) for x in
                                     user_data[user_id]['dates']])
            steps_to_add = np.array(user_data[user_id]['steps'])
            self.lines[idx].set_xdata(np.append(self.lines[idx].get_xdata(),
                                               dates_to_add))
            self.lines[idx].set_ydata(np.append(self.lines[idx].get_ydata(),
                                              steps_to_add))
        self.axes.relim()
        self.axes.autoscale_view()
        plt.show()
        self.fig.canvas.draw()

if __name__ == '__main__':
    user_data = {'a': {'dates': ['2017-09-01', '2017-09-02'], 'steps': [8068,
                                                                        5432.5]},
                 'b': {'dates': ['2017-09-01', '2017-09-02'], 'steps': [7000,
                                                                        10000]}}
    fbplt = fitbit_plotter(user_data)
    dates = ['2017-09-0' + str(x) for x in xrange(3,8)]
    for i in xrange(0,5):
        fbplt.add_data({'a': {'dates': [dates[i]], 
                              'steps': [randint(1000,15000)]},
                        'b': {'dates': [dates[i]],
                              'steps': [randint(1000,15000)]}})
        plt.pause(.1)
        sleep(1)

