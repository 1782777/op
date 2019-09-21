import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
from get_day_histroy import history
import matplotlib.font_manager as font_manager
from load_sina import LoadNet

his=history()
mean_data = his.get_dayMean()
ln= LoadNet()

mean_data['current']=0
mean_data['mean']=0
POINTS = 100
sin_list = [0] * POINTS
indx = 0
zx_index =[]

fig, ax = plt.subplots()
# ax.set_ylim([-2, 2])
# ax.set_xlim([0, POINTS])
# ax.set_autoscale_on(False)
#ax.set_xticks(range(0, 100, 10))
# ax.set_yticks(range(-2, 3, 1))
#ax.grid(True)

#line_sin, = ax.plot(mean_data, label='volume', color='cornflowerblue')
ax.legend(loc='upper center', ncol=4, prop=font_manager.FontProperties(size=8))
mean_data = mean_data.cumsum(axis=0)
print(mean_data)
diff_data =pd.DataFrame()
def sin_output(ax):
    ax.cla()
    global indx, sin_list, line_sin
    if indx == 20:
        indx = 0
    indx += 1
 
    sin_list = sin_list[1:] + [np.sin((indx / 10) * np.pi)]
    #print(sin_list)
    zx_index.append(indx)

    # line_sin.set_xdata(zx_index)
    # line_sin.set_ydata(np.sin(zx_index))

    a = ln.get_sz50_price()
    #a.cumsum(axis=0)
    str_time =a[31]
    str_volume =a[9]
    #print(str_time,str_volume)
    time =pd.datetime.strptime(str_time,'%H:%M:%S')
    #time = pd.to_datetime(str_time)
    # print(type(mean_data.index[0]))
    #print(type(time))
    #print(mean_data)
    mean_data['current'][mean_data.index>time.time()] = int(str_volume)/100000
    #print(mean_data['current'][mean_data.index>time.time()])
    #lasttime_frame['current'] = str_volume
    diff_data = mean_data.copy()
    diff_data['current'] = pd.to_numeric(diff_data['current']) 
    diff_data['current'] = diff_data['current'].diff(1)
    diff_data.iloc[0,1] =float( mean_data.iloc[0,1])
    print(mean_data)
    ax.plot(mean_data)

    #ax.draw_artist(line_sin)
    ax.figure.canvas.draw()
 
 
timer = fig.canvas.new_timer(interval=2000)
timer.add_callback(sin_output, ax)
timer.start()
plt.show()
