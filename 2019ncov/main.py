# -*- coding: utf-8 -*-

import time
import json
import requests
from datetime import datetime
import numpy as np
import matplotlib
import matplotlib.figure
from matplotlib.font_manager import FontProperties
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

plt.rcParams['font.sans-serif'] = ['FangSong']  # 设置默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像时'-'显示为方块的问题

def load_data():
    data = pd.read_csv('test.csv', index_col=0)
    data = data.fillna(0)
    time = list(data.index)


    return data, time

def catch_distribution(data, t):
    """抓取行政区域确诊分布数据"""

    #time = list(data.index)
    province = list(data.columns)
    data_dict = {}
    t = t
    for i in range(len(province)):
        data_dict[province[i]] = data.ix[t, province[i]]

    return data_dict


def plot_distribution():
    """绘制行政区域确诊分布数据"""

    data_total, time= load_data()
    for t in time:
        data = catch_distribution(data_total, t)



        font = FontProperties(fname='res/msyh.ttf', size=14)
        lat_min = 0
        lat_max = 60
        lon_min = 70
        lon_max = 140

        handles = [
            matplotlib.patches.Patch(color='#ffaa85', alpha=1, linewidth=0),
            matplotlib.patches.Patch(color='#ff7b69', alpha=1, linewidth=0),
            matplotlib.patches.Patch(color='#bf2121', alpha=1, linewidth=0),
            matplotlib.patches.Patch(color='#8e1b1b', alpha=1, linewidth=0),
            matplotlib.patches.Patch(color='#7f1818', alpha=1, linewidth=0),
            matplotlib.patches.Patch(color='#3c0d0d', alpha=1, linewidth=0),
        ]
        labels = ['1-9人', '10-99人', '100-299人', '300-499人', '500-999人', '>1000人']

        fig = matplotlib.figure.Figure()
        fig.set_size_inches(10, 9)  # 设置绘图板尺寸
        axes = fig.add_axes((0.1, 0.12, 0.8, 0.8))  # rect = l,b,w,h
        m = Basemap(llcrnrlon=lon_min, urcrnrlon=lon_max, llcrnrlat=lat_min, urcrnrlat=lat_max, resolution='l', ax=axes)
        m.readshapefile('res/china-shapefiles-master/china', 'province', drawbounds=True)
        m.readshapefile('res/china-shapefiles-master/china_nine_dotted_line', 'section', drawbounds=True)
        m.drawcoastlines(color='black')  # 洲际线
        m.drawcountries(color='black')  # 国界线
        m.drawparallels(np.arange(lat_min, lat_max, 10), labels=[1, 0, 0, 0])  # 画经度线
        m.drawmeridians(np.arange(lon_min, lon_max, 10), labels=[0, 0, 0, 1])  # 画纬度线

        for info, shape in zip(m.province_info, m.province):
            pname = info['OWNER'].strip('\x00')
            fcname = info['FCNAME'].strip('\x00')
            if pname != fcname:  # 不绘制海岛
                continue


            for key in data.keys():
                if key in pname:
                    if data[key] == 0:
                        color = '#f0f0f0'
                    elif data[key] < 10:
                        color = '#ffaa85'
                    elif data[key] < 100:
                        color = '#ff7b69'
                    elif data[key] < 300:
                        color = '#bf2121'
                    elif data[key] < 500:
                        color = '#8e1b1b'
                    elif data[key] < 1000:
                        color = '#7f1818'
                    else:
                        color = '#3c0d0d'
                    break

            poly = Polygon(shape, facecolor=color, edgecolor=color)
            axes.add_patch(poly)

        axes.legend(handles, labels, bbox_to_anchor=(0.5, -0.15), loc='lower center', ncol=3, prop=font)
        axes.set_title("2019-nCoV疫情地图", fontproperties=font)
        total = int(sum(list(data.values())))
        axes.text(123, 27, t, fontproperties=font, family='fantasy', fontsize=25
                  )
        axes.text(124, 21, '确诊人数', fontproperties=font, family='fantasy', fontsize=30
                  )
        axes.text(127, 14, total, family='fantasy', fontsize=30
                  )
        FigureCanvasAgg(fig)
        fig.savefig('pic/main/2019-nCoV疫情地图' + t + '.png')



if __name__ == '__main__':
    # plot_daily()
    plot_distribution()