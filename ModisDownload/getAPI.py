import json
import os
import random
import ssl
import time
from subprocess import run, PIPE
from urllib.request import urlopen, Request

import numpy as np
import pandas as pd
from tqdm import tqdm

from ModisDownload.domain import Sensor, DownLoadFile, Country


class HTTPF:
    """
    所有请求的父类
    """

    def __init__(self):
        self.user_agent = [
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
            "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
            "Opera/8.0 (Windows NT 5.1; U; en)",
            "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
            "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
            "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
            "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv,2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Mozilla/5.0 (Windows NT 6.1; rv,2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
            "MAC：Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36",
            "Windows：Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
            "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
            "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)"
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4094.1 Safari/537.36",
            "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
            "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
            "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
            "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
            "Mozilla/5.0 (Linux; U; Android 2.2.1; zh-cn; HTC_Wildfire_A3333 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
            "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
            "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
            "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
            "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
            "UCWEB7.0.2.37/28/999",
            "NOKIA5700/ UCWEB7.0.2.37/28/999",
            "Openwave/ UCWEB7.0.2.37/28/999",
            "Openwave/ UCWEB7.0.2.37/28/999",
        ]
        self.headers = {
            "User-Agent": self.get_userAgent()
        }
        self.creat_data_dir()

    def get_userAgent(self):
        return self.user_agent[random.randint(0, len(self.user_agent) - 1)]

    def can_visit(self, url):
        excecode = run("start /B ping " + url, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
        return excecode.returncode == 0

    def visit(self):
        pass

    def parse_answer(self):
        pass

    def creat_data_dir(self):
        create_path = os.path.dirname(__file__)+"/temp"
        if os.path.exists(create_path):
            pass
        else:
            os.mkdir(create_path)


class sensor(HTTPF):
    """
    查看传感器产品
    """

    def __init__(self):
        super().__init__()
        self.answer = []
        self.csv_list = []
        self.url = "https://ladsweb.modaps.eosdis.nasa.gov/api/v1/products/excludeBrowse=true"
        self.headers = {
            "User-Agent": self.get_userAgent()
        }
        self.jsonpath = os.path.dirname(__file__)+"/temp/sensor.json"
        self.csv_path = os.path.dirname(__file__)+"/temp/sensor.csv"
        self.pro_dict = {}

    def visit(self):
        ret = self.can_visited()
        assert ret, "网络连接失败请稍后再试！！"
        CTX = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        fh = urlopen(Request(self.url, headers=self.headers), context=CTX)
        with open(self.jsonpath, "wb") as f:
            f.write(fh.read())
        f.close()
        return

    def parse_answer(self):
        assert os.path.exists(self.jsonpath), "请更新传感器目录！！"
        with open(self.jsonpath, 'r') as load_f:
            load_dict = json.load(load_f)
        for i in tqdm(range(len(load_dict))):
            Sens = Sensor()
            for (key, value) in load_dict[i].items():
                if dir(Sens).__contains__(key):
                    setattr(Sens, key, value)
                else:
                    print(key + " is not in Sensor Class !! please update packages")
            self.answer.append(Sens)
            self.csv_list.append(str(Sens).strip('"').split(","))
        pd.DataFrame(self.csv_list).to_csv(self.csv_path, index=False)
        self.init_dict()
        return self.answer

    def can_visited(self):
        return self.can_visit(self.url)

    def init_dict(self):
        if not os.path.exists(self.csv_path):
            print("正在更新传感器目录")
            self.visit()
            self.parse_answer()
        data = pd.read_csv(self.csv_path, index_col=None, sep=",")

        for i in np.array(data):
            self.pro_dict.update({
                i[0]: i[1].split(":")
            })
        return


class geo(HTTPF):
    def __init__(self):
        super().__init__()
        self.dict_ans = {}
        self.url = "https://ladsweb.modaps.eosdis.nasa.gov/search/geodata/world_countries.geojson"
        self.country_path = os.path.dirname(__file__)+"/temp/country.json"
        self.json_path = os.path.dirname(__file__)+"/temp/geo.json"
        self.answer = {

        }

    def visit(self):
        def parse_json():
            with open(self.json_path, "r") as f:
                dict = json.load(f)
            for i in dict["features"]:
                country_ = Country(i)
                if not country_.canuse:
                    continue
                if self.answer.__contains__(country_.CNTRY_NAME):
                    self.answer[country_.CNTRY_NAME].append(str(country_))
                else:
                    self.answer.update({
                        country_.CNTRY_NAME: [str(country_)]
                    })
            return

        ret = self.can_visited()
        assert ret, "网络连接失败请稍后再试！！"
        CTX = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        fh = urlopen(Request(self.url, headers=self.headers), context=CTX)
        temp = fh.read()
        with open(self.json_path, "wb") as f:
            f.write(temp)
        f.close()
        parse_json()

        with open(self.country_path, "w") as f:
            f.write(json.dumps(self.answer))
        f.close()
        return

    def can_visited(self):
        return self.can_visit(self.url)

    def parse_answer(self):
        if not os.path.exists(self.country_path):
            print("初始化地区列表")
            self.visit()
        with open(self.country_path, "r") as f:
            self.answer = json.load(f)
        f.close()
        return

    def getAreaList(self, name):
        if self.answer.__contains__(name):
            return self.answer.get(name)
        else:
            print("没有此国家和地区！！")
            return []


class searchData:
    def __init__(self, production: str, date: str, area: str, sens: sensor, g: geo):
        self.production = production
        self.dates = date
        self.collections = []
        self.area = area
        self.area_list = None
        self.sens = sens
        self.g = g
        self.check()

    def check(self):
        assert self.sens.pro_dict.__contains__(self.production), "产品名称错误"
        self.collections = self.sens.pro_dict[self.production]
        if self.g.answer.__contains__(self.area):
            self.area_list = self.g.answer.get(self.area)
        else:
            self.area_list = [self.area]
        return


class search(HTTPF):
    """
    查询主方法
    """

    def __init__(self, searchdata: searchData):
        super().__init__()
        self.url = "https://ladsweb.modaps.eosdis.nasa.gov/api/v1/files/product="
        self.headers = {
            "User-Agent": self.get_userAgent()
        }
        self.searchdata = searchdata
        self.url_List = []
        self.answer = []
        self.file_name_path = os.path.dirname(__file__)+"/temp/" + str(time.time()) + ".csv"
        self.downList = []
        self.canuse=False


    def make_post_url(self):
        for area in self.searchdata.area_list:
            for collection in self.searchdata.collections:
                try:
                    temp = self.url + self.searchdata.production + "&collection=" + collection + "&dateRanges=" + \
                           self.searchdata.dates + "&areaOfInterest=" + area + "&dayCoverage=true&dnboundCoverage=true"
                    self.url_List.append(temp)
                    CTX = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
                    fh = urlopen(Request(temp, headers=self.headers), context=CTX)
                    self.answer.append(fh.read())
                    print("查询：" + temp)
                except:
                    print("网络异常！！")
        return

    def parse_answer(self):
        for js in self.answer:
            temp = json.loads(js)
            if isinstance(temp,dict):
                for key in temp.keys():
                    self.downList.append(DownLoadFile(temp.get(key)))
        if len(self.downList)==0:
            return
        pd.DataFrame([str(i).strip('"').split(",") for i in self.downList]).to_csv(self.file_name_path, header=None,
                                                                                   index_label=None, index=False)
        self.canuse=True
        return

    def can_visited(self):
        return self.can_visit(self.url)
