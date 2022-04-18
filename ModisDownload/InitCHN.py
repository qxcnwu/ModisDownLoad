# -*- coding: utf-8 -*-
# @Time    : 2022/5/21 23:49
# @Author  : qxcnwu
# @FileName: InitCHN.py
# @Software: PyCharm

import json
import os
import ssl
from urllib.error import HTTPError, URLError
from urllib.request import urlopen, Request

from tqdm import tqdm


def get_header(length:int):
    return {
        "Host": "36.112.130.153:7777",
        "Connection": "keep-alive",
        "Content-Length": length,
        "Accept": "application/json,text/plain,*/*",
        "DNT": "1",
        "access-agent": "pc-dss",
        "murmur": "96caaa0f25088aaa1f35de3c8dc73814",
        "User-Agent": "Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/101.0.4951.64Safari/537.36Edg/101.0.1210.53",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "http//36.112.130.153:7777",
        "Referer": "http://36.112.130.153:7777/",
        "Accept-Encoding": "gzip,deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"
    }

class Init:
    def __init__(self,reInit=False):
        super().__init__()
        self.reInit=reInit
        path = os.path.dirname(__file__) + "/temp"
        if not os.path.exists(path):
            os.makedirs(path)
        self.sentinal_url = "http://36.112.130.153:7777/manage/meta/api/metadatas/fields?field=all"
        self.sentinal_csv=os.path.dirname(__file__)+"/temp/sentinel.json"

        self.sentinal_ans=None
        self.sentinals=[]
        self.type_url="http://36.112.130.153:7777/manage/meta/api/metadatas/satellites"
        self.type_list={"GX":[],"LD":[],"DQ":[],"DC":[],"JG":[]}
        self.type_ans={}

        self.should_update()

    def should_update(self):
        """
        判断是否需要更新
        Returns:
        """
        if os.path.exists(self.sentinal_csv) and not self.reInit:
            pass
        else:
            # self.get_sentinel()
            # 仅仅只需要通过type得到
            self.get_type()
        self._init()
        return

    def get_sentinel(self):
        CTX = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        try:
            print("正在更新传感器列表")
            fh = urlopen(Request(self.sentinal_url, headers=get_header(0)), context=CTX)
            self.sentinal_ans = fh.read()
            print("更新传感器列表成功")
        except HTTPError as e:
            print('HTTP GET error : ', e)
            pass
        except URLError as e:
            print('Failed to make request:', e)
        return

    def get_type(self):
        def parse(request):
            sen_list=[]
            for i in request["result"]:
                for sensor in i["sensor"]:
                    sen_list.append(i["satellite"]+"_"+sensor)
            return sen_list
        print("正在更新传感器类型列表")
        for tp in tqdm(self.type_list.keys()):
            CTX = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            temp_json={"type":tp}
            try:
                data=json.dumps(temp_json).encode("utf-8")
                fh = urlopen(Request(self.type_url, headers=get_header(len(data)),data=data), context=CTX)
                self.sentinal_ans = fh.read()
                temp=json.loads(self.sentinal_ans.decode("utf-8"))
                self.type_list[tp]=parse(temp)
            except HTTPError as e:
                print('HTTP GET error : ', e)
                return
            except URLError as e:
                print('Failed to make request:', e)
                return
        print("正在更新传感器类型列表完成")
        for key,vals in self.type_list.items():
            for val in vals:
                self.type_ans.update({
                    val:key
                })
        self._parse()
        return

    def _parse(self):
        with open(self.sentinal_csv,"w") as fd:
            fd.write(json.dumps(self.type_ans))
        fd.close()
        return

    def _init(self):
        with open(self.sentinal_csv, "r") as fd:
            self.type_ans=json.loads(fd.read())
        self.sentinals=self.type_ans.keys()
        return

    def get_sentinels(self):
        return self.type_ans.keys()

if __name__ == '__main__':
    a=Init()
