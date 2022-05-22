import os
from multiprocessing import Process
import pandas as pd
import numpy as np
import json

from ModisDownload.WatchDir import watch_dir_size
from ModisDownload.downloadMain import download_main
from ModisDownload.getAPI import sensor, search, searchData, geo

class getHtml:
    def __init__(self, token):
        print("查询前请确保Token字符串的有效性！具体消息请访问 https://ladsweb.modaps.eosdis.nasa.gov/#generate-token")
        self.answer = []
        self.update = False
        self.token = token
        self.sensor = self.get_sensor()
        self.g = self.get_geo()

    def get_sensor(self, refresh=False):
        """
        获取传感器参数
        :param refresh: 是否重新初始化
        :return:
        """
        self.update = True
        sens = sensor()
        if refresh:
            sens.visit()
            sens.parse_answer()
        else:
            if not os.path.exists(sens.csv_path):
                self.get_sensor(True)
        sens.init_dict()
        return sens

    def get_geo(self):
        g = geo()
        g.parse_answer()
        return g

    def get_search(self, sensor_name: str, date: str, area: str):
        """
        查询
        :param sensor_name:
        :param date:
        :return:
        """
        searchdata = searchData(sensor_name, date, area, self.sensor, self.g)
        sea = search(searchdata)
        sea.make_post_url()
        sea.parse_answer()
        return sea

    def download_main(self, sensor_name: str, dates: str,area:str, download_dir, **kwargs):
        """
        下载
        :param sensor_name:
        :param dates:
        :param download_dir:
        :return:
        """
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        sea = self.get_search(sensor_name, dates,area.lower())
        if not sea.canuse:
            print("未查询到可下载数据")
            return
        p = Process(target=watch_dir_size, args=(download_dir, sea.file_name_path))
        p.start()
        download_main(download_dir, self.token, sea.file_name_path, **kwargs)
        return

def reload():
    origin=os.path.dirname(__file__)+"/temp"
    for file in os.listdir(origin):
        try:
            os.remove(os.path.join(origin,file))
        except:
            pass
    print("重新初始化完成")
    return

def search_p():
    getHtml("")
    origin = os.path.dirname(__file__) + "/temp/sensor.csv"
    data=np.array(pd.read_csv(origin,header=None,index_col=False))
    for idx,i in enumerate(data):
        print(idx," ",i)
    return data

def search_area():
    getHtml("")
    origin = os.path.dirname(__file__) + "/temp/country.json"
    with open(origin,"r") as fd:
        dicts=json.load(fd)
    for key,value in dicts.items():
        print(key,":",value)
    return dicts
