# -*- coding: utf-8 -*-
# author QXC NWU
# TIME 2022/4/13

import os
import ssl
import threading
from retry import retry
import multitasking as multitasking
import numpy as np
import pandas as pd
import requests
from tqdm import tqdm
from multiprocessing import Process


class DownLoadThread:
    def __init__(self, url: str, token: str, save_path: str, split_block: int, retry_times=3):
        self.url = url
        self.save_path = save_path
        self.split_block = split_block
        self.can_thread = True
        self.retry_time = retry_times
        self.headers = {
            'user-agent': 'tis/download.py_1.0--3.7.6rc1 (tags/v3.7.6rc1:bd18254b91, Dec 11 2019, 20:31:07) [MSC v.1916 64 bit (AMD64)]',
            'Authorization': 'Bearer ' + token
        }
        # 获取文件大小
        self.size = self.get_file_size()

    def split(self, end, step):
        """
        文件分块
        :param end: 结束大小
        :param step: 步长
        :return:
        """
        return [(start, min(start + step, end)) for start in range(0, end, step)]

    def get_file_size(self):
        """
        获取文件大小
        :return:
        """
        response = requests.head(self.url, headers=self.headers)
        file_size = response.headers.get('Content-Length')
        if (file_size == None):
            self.can_thread = False
            return None
        return int(file_size)

    def download_main(self):
        f = open(self.save_path, 'wb')

        @retry(tries=self.retry_time)
        @multitasking.task
        def start_download(start: int, end: int):
            """
            分段下载
            :param start: 开始位置
            :param end: 结束位置
            :return:
            """
            _headers = self.headers
            # 分段下载的核心
            _headers['Range'] = f'bytes={start}-{end}'
            # 发起请求并获取响应（流式）
            requests.packages.urllib3.disable_warnings()
            response = session.get(self.url, headers=_headers, stream=True, verify=False)
            # 每次读取的流式响应大小
            chunk_size = 1280
            # 暂存已获取的响应，后续循环写入
            chunks = []
            for chunk in response.iter_content(chunk_size=chunk_size):
                # 暂存获取的响应
                chunks.append(chunk)
                # 更新进度条
                bar.update(chunk_size)
            f.seek(start)
            for chunk in chunks:
                f.write(chunk)
            # 释放已写入的资源
            del chunks

        session = requests.Session()
        # 分块文件如果比文件大，就取文件大小为分块大小
        each_size = min(self.size, self.split_block)
        # 分块
        parts = self.split(self.size, each_size)
        # 创建进度条
        bar = tqdm(total=self.size, desc=f'下载文件：{self.save_path}')
        for part in parts:
            start, end = part
            start_download(start, end)
        # 等待全部线程结束
        multitasking.wait_for_tasks()
        f.close()
        bar.close()
        return


def read_csv(csv_path: str, save_dir: str) -> [list, list]:
    """
    # 创建文件名称池文件大小池
    :param csv_path: csv文件路径 默认格式 文件名：日期：文件大小
    :param save_dir: 保存路径
    :return: filename_list,save_list
    """
    data = np.array(pd.read_csv(csv_path, header=None, index_col=None))
    filename_list = data[:, 2].tolist()
    save_list = [os.path.join(save_dir, i) for i in data[:, 0].tolist()]
    fileLength=data[:,1].tolist()
    dic = {}
    for idx, i in enumerate(data[:, 0]):
        dic.update({
            i: [filename_list[idx], save_list[idx],int(fileLength[idx])]
        })
    return dic


def get_file(filename: str, save_path: str, url: str, token: str, multThread=False):
    """
    # 下载文件函数
    :param filename: 文件名
    :param save_path: 保存文件路径
    :return: null
    """
    # URL修改位置
    url = url + filename
    # Token修改位置 Bearer
    headers = {
        'user-agent': 'tis/download.py_1.0--3.7.6rc1 (tags/v3.7.6rc1:bd18254b91, Dec 11 2019, 20:31:07) [MSC v.1916 64 bit (AMD64)]',
        'Authorization': 'Bearer ' + token
    }
    if multThread:
        downLoadThread = DownLoadThread(url, token, save_path, 1024 ** 2, 3)
        downLoadThread.download_main()
    else:
        CTX = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        from urllib.request import urlopen, Request, URLError, HTTPError
        try:
            fh = urlopen(Request(url, headers=headers), context=CTX)
            with open(save_path, "wb") as f:
                f.write(fh.read())
            f.close()
        except HTTPError as e:
            # print(save_path + " will be redownload later")
            # print('HTTP GET error : ',e)
            pass
        except URLError as e:
            pass
            # print(save_path + " will be redownload later")
            # print('Failed to make request:',e)
        return None


def threading_download(filename_list: list, save_list: list, url: str, token: str):
    """
    # 多线程下载
    :param thread_num:线程数量
    :param filename_list:文件池
    :param save_list:保存池
    :param filesize_list:大小池
    :return:Null
    """
    threads = []
    u = len(filename_list)
    for i in range(u):
        t = threading.Thread(target=get_file, args=(filename_list[i], save_list[i], url, token))
        threads.append(t)
    for i in range(u):
        threads[i].start()
    for i in range(u):
        threads[i].join()
    return


def no_thread_download(filename_list: list, save_list: list, url: str, token: str):
    for i in range(len(filename_list)):
        get_file(filename_list[i], save_list[i], url, token)
    return


def log_check(file_dict: dict, thread_num: int, save_dir: str, url: str, token: str,check_size=False) -> bool:
    """
    # 搜索失败的下载量
    :param csv_path: csv路径
    :param thread_num: 线程数量
    :param save_dir: 保存路径
    :return: Bool操作
    """
    filename_list = [i[0] for i in file_dict.values()]
    save_list = [i[1] for i in file_dict.values()]
    all = len(file_dict)
    files = os.listdir(save_dir)
    if not check_size:
        for file in files:
            if file in file_dict.keys() and os.path.getsize(os.path.join(save_dir, file)) !=0:
                filename_list.remove(file_dict[file][0])
                save_list.remove(file_dict[file][1])
    else:
        for file in files:
            if file in file_dict.keys() and os.path.getsize(os.path.join(save_dir, file)) == file_dict[file][2]:
                filename_list.remove(file_dict[file][0])
                save_list.remove(file_dict[file][1])
    if len(filename_list) == 0:
        return False
    else:
        print("总共有", all, "个文件，下载完成", all - len(filename_list), "个")
        MutiProcessMain(filename_list,save_list, url, token,thread_num)
        return True


def MutiProcessMain(filename_list,save_list, url, token ,MutiNum=4):
    number=len(filename_list)
    if number<=MutiNum:
        threading_download(filename_list,save_list, url, token)
    else:
        pList=[]
        number=number//MutiNum
        for i in range(MutiNum):
            if i==MutiNum-1:
                p=Process(target=threading_download,args=(filename_list[i*number:],save_list[i*number:], url, token))
            else:
                p=Process(target=threading_download,args=(filename_list[i*number:(i+1)*number],save_list[i*number:], url, token))
            p.start()
            pList.append(p)
        for p in pList:
            p.join()
        return


def download_main(save_dir: str, token: str, csv_path: str, thread_num=5, url="https://ladsweb.modaps.eosdis.nasa.gov",
                  max_try=10):
    """
    # 下载主函数
    :param url: URL
    :param save_dir: 保存路径
    :param token: TOKEN
    :param csv_path: csv路径
    :param thread_num: 线程数量
    :param max_try: 最大轮询数量
    :return:
    """
    logflag = True
    file_dic = read_csv(csv_path, save_dir)
    while logflag or max_try == 0:
        print("剩余下载轮询次数", max_try)
        max_try -= 1
        logflag = log_check(file_dic, thread_num, save_dir, url, token)
    print("检查下载文件完整性")
    log_check(file_dic, thread_num, save_dir, url, token,check_size=True)
    print("下载完成")
