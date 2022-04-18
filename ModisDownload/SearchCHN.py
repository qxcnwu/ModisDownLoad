# -*- coding: utf-8 -*-
# author QXC NWU
# TIME 2022/4/13

import json
import ssl
from typing import List
from urllib.error import HTTPError, URLError
from urllib.request import urlopen, Request

import pandas as pd
from tqdm import tqdm

from ModisDownload.Base import Base, Sensors


class SearchData(Base):
    def __init__(self, startdate: str, enddate: str, sensors: List[Sensors], position: List[str], cloud: int,
                 productlev: int):
        """
        组装多个不同的传感器，地理位置
        """
        super().__init__()
        self.jsonlist = []
        self.startdate = startdate
        self.enddate = enddate
        self.sensors = sensors
        self.position = position
        self.cloud = cloud
        self.productlev = productlev
        self.type_lists = {"GX": [], "LD": [], "DQ": [], "DC": [], "JG": []}
        self._make_json()

    def _make_json(self):
        for i in self.sensors:
            temp_sensors = self.type.get(i.name)
            for j in self.position:
                self.jsonlist.append({
                    "page": 1,
                    "size": 200 * 365,
                    "geom": [j],
                    "scenetime": [
                        self.startdate,
                        self.enddate
                    ],
                    "satelliteSensor": [i.name],
                    "prodlevel": self.productlev,
                    "cloudpsd": self.cloud,
                    "dwxtype": temp_sensors,
                    "userType": "0",
                    "userId": self._get_ip(),
                    "crossed": "false",
                    "desc": [
                        "scenetime"
                    ]
                })
        return


class SearchChina(Base):
    def __init__(self, searchData: SearchData, show_proc=False):
        """
        查询产品类
        Args:
            searchData:查询对象
        """
        super().__init__()

        # check sensors in sensors list
        self.show_proc = show_proc
        self._json = searchData.jsonlist
        self.answer = None
        self.dict = None
        self.result = []
        self.header = None
        self.pdfram = None

    def search(self):
        for i in tqdm(self._json):
            self._upload(i)
        return

    def _upload(self, js):
        """
        查询
        Returns: None
        """

        def encode():
            _json = json.dumps(js)
            _json = _json.replace("\n", "")
            return _json.encode("utf-8")

        jsonBytes = encode()
        CTX = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        try:
            print("正在查询")
            fh = urlopen(Request(self.url, headers=self._get_header(len(jsonBytes)), data=jsonBytes), context=CTX)
            self.answer = fh.read()
            self._parse()
            print("查询成功")
        except HTTPError as e:
            print('HTTP GET error : ', e)
            pass
        except URLError as e:
            print('Failed to make request:', e)
        except Exception as e:
            print(e)
        return

    def _parse(self):
        self.dict = json.loads(self.answer)
        if self.dict is None:
            print("未查询到任何产品")
            return
        if int(self.dict["size"]) == 0:
            print("未查询到任何产品")
            return
        self.header = [i for i in self.dict["result"][0].keys()]
        for item in self.dict["result"]:
            self.result.append([i for i in item.values()])
        self.pdfram = pd.DataFrame(self.result, columns=self.header)
        if self.show_proc:
            self._show()
        return

    def _show(self):
        print(self.header)
        for i in self.result:
            print(i)
        return

    def save_ans(self, save_path):
        """
        保存查询结果
        Args:
            save_path: 保存路径
        Returns:
        """
        if self.pdfram is None:
            print("未查询到任何结果")
            return
        self.pdfram.to_csv(save_path, index=None)
        return

    def get_size(self):
        """
        获取结果集大小
        Returns:

        """
        return self.dict["size"]

