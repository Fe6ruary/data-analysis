# -*- coding: utf-8 -*-
# 可用
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
from pypinyin import lazy_pinyin
import os
from tqdm import tqdm

plt.rcParams['font.sans-serif'] = ['FangSong']  # 设置默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像时'-'显示为方块的问题


def load_data():
    data = pd.read_csv('city_new.csv')
    rule = pd.read_csv('rule.csv')
    time = list(set(list(data.date)))

    rule_ = {}
    for i in range(len(rule)):
        rule_[rule.ix[i, 'city']] = rule.ix[i, 'pinyin'] #字典形式

    return data, rule_, time


def catch_distribution(data, t, rule_):
    """抓取行政区域确诊分布数据"""

    data_dict = {}
    t = t

    df = data[data['date'] == t]

    city_ = list(df.city)
    num_ = list(df.confirmed)

    for i in range(len(df)):
        if city_[i] in rule_.keys():  #规则修正
            try:
                low = str.lower(rule_[city_[i]])
                data_dict[low] = num_[i]
                continue
            except:
                print(rule_[city_[i]])
                continue

        l = lazy_pinyin(city_[i])
        py = ''.join(l)
        data_dict[py] = num_[i]

    return data_dict


# 获取各省经纬度
def lat_lon(province_i, provinceLocation):
    df = province_i[province_i['province'] == provinceLocation]

    lat_min = df.lat_min.values[0]
    lat_max = df.lat_max.values[0]
    lon_min = df.lon_min.values[0]
    lon_max = df.lon_max.values[0]
    print(lat_min, lat_max, lon_min, lon_max)

    return lat_min, lat_max, lon_min, lon_max


def plot_distribution():
    """绘制行政区域确诊分布数据"""

    province_i = pd.read_csv('province_location.csv')  # 各省经纬度范围

    #provinceLocation = list(province_i['province'])  # 拼音
    #provinceLocation = ['Hubei', 'Zhejiang', 'Guangdong', 'Henan', 'Hunan', 'Anhui', 'Jiangxi', 'Chongqing', 'Jiangsu', 'Sichuan', 'Shandong']
    provinceLocation = [ 'Zhejiang']
    #provinceLocation = ['Guangdong', 'Henan', 'Hunan', 'Anhui', 'Jiangxi', 'Jiangsu',
     #                   'Sichuan', 'Shandong']
    #provinceLocation_CH = list(province_i['province_CH'])  # 中文
    #provinceLocation_CH = ['湖北', '浙江', '广东', '河南', '湖南', '安徽', '江西', '重庆', '江苏', '四川', '山东']
    provinceLocation_CH = ['浙江']

    for i in tqdm(range(len(provinceLocation))):
        lat_min, lat_max, lon_min, lon_max = lat_lon(province_i, provinceLocation[i])

        font = FontProperties(fname='res/msyh.ttf', size=12)

        data_total, rule, time = load_data()

        time = pd.date_range('2020-01-21', '2020-2-12')

        time = time.strftime('%Y-%m-%d')

        time = list(time)

        for t in time:
            data = catch_distribution(data_total, t, rule)


            handles = [
                matplotlib.patches.Patch(color='#f0ccc9', alpha=1, linewidth=0),
                matplotlib.patches.Patch(color='#d9847d', alpha=1, linewidth=0),
                matplotlib.patches.Patch(color='#b4483e', alpha=1, linewidth=0),
                matplotlib.patches.Patch(color='#8e2218', alpha=1, linewidth=0),
                matplotlib.patches.Patch(color='#560a03', alpha=1, linewidth=0),
                matplotlib.patches.Patch(color='#160301', alpha=1, linewidth=0),
            ]
            labels = ['1-9人', '10-29人', '30-49人', '50-99人', '100-249人', '>250人']

            fig = plt.figure()
            fig.set_size_inches(10, 11)  # 设置绘图板尺寸
            axes = fig.add_axes([0.1, 0.1, 0.8, 0.8])

            total = 0 #今日人数



            try:

                m = Basemap(llcrnrlon=lon_min, urcrnrlon=lon_max, llcrnrlat=lat_min, urcrnrlat=lat_max, resolution='l',
                            ax=axes)
                m.readshapefile('res/CHN_adm_shp/CHN_adm3', 'states', drawbounds=False)
                m.readshapefile('res/china-shapefiles-master/china_nine_dotted_line', 'section', drawbounds=True)
                #m.drawcoastlines()  # 海岸线
                m.drawcountries()  # 洲际线
                m.drawparallels(np.arange(lat_min, lat_max, 2), labels=[1, 0, 0, 0])  # 经度线
                m.drawmeridians(np.arange(lon_min, lon_max, 2), labels=[0, 0, 0, 1])  # 纬度线

                for info, shape in zip(m.states_info, m.states):
                    proid = info['NAME_1']

                    if (proid == 'Chongqing') | (proid == 'Shanghai'):
                        city = info['NAME_3']
                        city = str.lower(city)
                    else:
                        city = info['NAME_2']
                        city = str.lower(city)

                    if city not in data.keys():
                        continue

                    if proid == provinceLocation[i]:
                        for key in data.keys():
                            if key == city:
                                if data[key] == 0:
                                    color = '#f0f0f0'
                                elif data[key] < 10:
                                    color = '#f0ccc9'
                                elif data[key] < 30:
                                    color = '#d9847d'
                                elif data[key] < 50:
                                    color = '#b4483e'
                                elif data[key] < 100:
                                    color = '#8e2218'
                                elif data[key] < 250:
                                    color = '#560a03'
                                else:
                                    color = '#160301'

                                total += data[key]

                        poly = Polygon(shape, facecolor=color, edgecolor='b', lw=0.2)
                        axes.add_patch(poly)


                m.readshapefile('res/china-shapefiles-master/china', 'province', drawbounds=True)


                axes.legend(handles, labels, bbox_to_anchor=(0.5, -0.2), loc='lower center', ncol=3, prop=font)
                axes.set_title("2019-nCoV疫情地图-"+ provinceLocation_CH[i], fontproperties=font)

                axes.text(lon_max-2, lat_max+0.2, t, fontproperties=font, family='fantasy', fontsize=25
                              )
                #axes.text(lon_max-1, lat_min+0.6, '确诊人数', fontproperties=font, family='fantasy', fontsize=30
                 #             )
                #axes.text(lon_max-1, lat_min+0.3, total, family='fantasy', fontsize=30
                 #            )
                #FigureCanvasAgg(fig)

                path = os.path.join(os.getcwd(), 'pic', provinceLocation[i])
                isExists = os.path.exists(path)

                if not isExists:
                    os.makedirs(path)

                plt.savefig(path + '/' + provinceLocation[i] + t + '.png', dpi=100)
                plt.close()

            except:
                print(provinceLocation[i])


if __name__ == '__main__':
    plot_distribution()