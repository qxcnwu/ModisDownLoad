import os
import time
from os.path import getsize, join
from tqdm import tqdm
import numpy as np
import pandas as pd

def watch_dir_size(save_dir:str,csv_path:str):
    data = np.array(pd.read_csv(csv_path, header=None, index_col=None))
    temp_dict={}
    files=os.listdir(save_dir)
    for idx,i in enumerate(data[:,0]):
        if i in files and os.path.getsize(os.path.join(save_dir, i)) !=0:
            continue
        else:
            temp_dict.update({
                i:data[idx,1]
            })
    total_size=sum(temp_dict.values())

    def getdirsize(dir):
        size = 0
        for root, dirs, files in os.walk(dir):
            size += sum([getsize(join(root, name)) for name in files])
        return size
    assert os.path.exists(save_dir),"文件夹"+save_dir+"不存在"
    muti_size=getdirsize(save_dir)
    size=muti_size
    old_size=size
    bar = tqdm(total=total_size, desc=f'文件监控：{save_dir}')
    while(size<muti_size+total_size):
        time.sleep(1)
        size=getdirsize(save_dir)
        bar.update(size-old_size)
        old_size=size
    bar.close()
