# -*- coding: utf-8 -*-
# @Time    : 2022/5/22 9:30
# @Author  : qxcnwu
# @FileName: Base.py
# @Software: PyCharm
import os
import random
from enum import Enum
from ModisDownload.InitCHN import Init

class Base:
    def __init__(self):
        self.url = "http://36.112.130.153:7777/manage/meta/api/metadatas/records"
        self.ip = [
            [607649792, 608174079],
            [1038614528, 1039007743],
            [1783627776, 1784676351],
            [2035023872, 2035154943],
            [2078801920, 2079064063],
            [-1950089216, -1948778497],
            [-1425539072, -1425014785],
            [-1236271104, -1235419137],
            [-770113536, -768606209],
            [-569376768, -564133889]
        ]
        path=os.path.dirname(__file__)+"/temp"
        if not os.path.exists(path):
            os.makedirs(path)
        init = Init()
        self.sentinels = init.get_sentinels()
        self.type=init.type_ans

    def _get_ip(self):
        ipdump = self.ip[random.randint(0, len(self.ip)-1)]
        ip = random.randint(ipdump[0], ipdump[0] + random.randint(0, ipdump[1] - ipdump[0]))
        strip = ""
        strip = strip + str((ip >> 24) & 0xff) + "."
        strip = strip + str((ip >> 16) & 0xff) + "."
        strip = strip + str((ip >> 8) & 0xff) + "."
        strip = strip + str(ip & 0xff)
        return strip

    def _get_header(self, length: int):
        return {
            "Host": "36.112.130.153:7777",
            "Connection": "keep-alive",
            "Content-Length": length,
            "ipaddr": self._get_ip(),
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

class Sensors(Enum):
    CSES_TBB= 'CSES_TBB'
    CSES_EFD= 'CSES_EFD'
    CSES_SCM= 'CSES_SCM'
    CSES_HPM= 'CSES_HPM'
    CSES_LAP= 'CSES_LAP'
    CSES_PAP= 'CSES_PAP'
    CSES_GRO= 'CSES_GRO'
    CSES_HEP= 'CSES_HEP'
    CBERS2B_WFI= 'CBERS2B_WFI'
    CBERS2B_CCD= 'CBERS2B_CCD'
    CBERS2B_HR= 'CBERS2B_HR'
    DQ1_PSS= 'DQ1_PSS'
    DQ1_ACDL= 'DQ1_ACDL'
    DQ1_WSI= 'DQ1_WSI'
    DQ1_DPC= 'DQ1_DPC'
    DQ1_EMI= 'DQ1_EMI'
    DQ1_POSP= 'DQ1_POSP'
    ZY303_PMS= 'ZY303_PMS'
    ZY303_NAD= 'ZY303_NAD'
    ZY303_MUX= 'ZY303_MUX'
    ZY303_TLC= 'ZY303_TLC'
    ZY303_FWD= 'ZY303_FWD'
    ZY303_BMS= 'ZY303_BMS'
    ZY303_BWD= 'ZY303_BWD'
    ZY303_DLC= 'ZY303_DLC'
    ZY303_DMS= 'ZY303_DMS'
    ZY303_TMS= 'ZY303_TMS'
    SCSY1_HIS= 'SCSY1_HIS'
    GFDM01_SMAC= 'GFDM01_SMAC'
    GFDM01_PMS= 'GFDM01_PMS'
    ZY302_MUX= 'ZY302_MUX'
    ZY302_NAD= 'ZY302_NAD'
    ZY302_PMS= 'ZY302_PMS'
    ZY302_TLC= 'ZY302_TLC'
    ZY302_TMS= 'ZY302_TMS'
    ZY302_DLC= 'ZY302_DLC'
    HJ1B_CCD= 'HJ1B_CCD'
    HJ1B_IRS= 'HJ1B_IRS'
    HJ1A_CCD= 'HJ1A_CCD'
    HJ1A_HSI= 'HJ1A_HSI'
    ZY3_TLC= 'ZY3_TLC'
    ZY3_NAD= 'ZY3_NAD'
    ZY3_BWD= 'ZY3_BWD'
    ZY3_MUX= 'ZY3_MUX'
    ZY3_FWD= 'ZY3_FWD'
    HJ1C_SAR= 'HJ1C_SAR'
    ZY1E_VNIC= 'ZY1E_VNIC'
    ZY1E_AHSI= 'ZY1E_AHSI'
    LT1B_SAR= 'LT1B_SAR'
    LT1A_SAR= 'LT1A_SAR'
    CBERS01_WFI= 'CBERS01_WFI'
    CBERS01_CCD= 'CBERS01_CCD'
    CBERS01_IRS= 'CBERS01_IRS'
    CBERS02_IRS= 'CBERS02_IRS'
    CBERS02_WFI= 'CBERS02_WFI'
    CBERS02_CCD= 'CBERS02_CCD'
    ZY1F_AHSI= 'ZY1F_AHSI'
    ZY1F_VNIC= 'ZY1F_VNIC'
    ZY1F_IRS= 'ZY1F_IRS'
    LT1AB_SAR= 'LT1AB_SAR'
    GF5B_DPC= 'GF5B_DPC'
    GF5B_GMI= 'GF5B_GMI'
    GF5B_AHSI= 'GF5B_AHSI'
    GF5B_VIMI= 'GF5B_VIMI'
    GF5B_POSP= 'GF5B_POSP'
    GF5B_AAS= 'GF5B_AAS'
    GF5B_PSS= 'GF5B_PSS'
    GF5B_EMI= 'GF5B_EMI'
    GF3C_SAR= 'GF3C_SAR'
    GF3B_SAR= 'GF3B_SAR'
    GF1C_PMS= 'GF1C_PMS'
    CB04A_MUX= 'CB04A_MUX'
    CB04A_WPM= 'CB04A_WPM'
    CB04A_WFI= 'CB04A_WFI'
    HJ2A_IRS= 'HJ2A_IRS'
    HJ2A_HSI= 'HJ2A_HSI'
    HJ2A_CCD= 'HJ2A_CCD'
    HJ2A_PSAC= 'HJ2A_PSAC'
    GF1B_PMS= 'GF1B_PMS'
    GF2_PMS= 'GF2_PMS'
    GJ1A_PMS= 'GJ1A_PMS'
    GF1D_PMS= 'GF1D_PMS'
    GF1_PMS= 'GF1_PMS'
    GF1_WFV= 'GF1_WFV'
    HJ2B_IRS= 'HJ2B_IRS'
    HJ2B_HSI= 'HJ2B_HSI'
    HJ2B_CCD= 'HJ2B_CCD'
    HJ2B_PSAC= 'HJ2B_PSAC'
    GJ1C_PMS= 'GJ1C_PMS'
    GF4_B1= 'GF4_B1'
    GF4_B3= 'GF4_B3'
    GF4_B2= 'GF4_B2'
    GF4_B4= 'GF4_B4'
    GF4_PMS= 'GF4_PMS'
    GF4_PI= 'GF4_PI'
    GF4_PMI= 'GF4_PMI'
    GF4_IRS= 'GF4_IRS'
    GF4_B5= 'GF4_B5'
    GJ1B_PMS= 'GJ1B_PMS'
    GF3_SAR= 'GF3_SAR'
    GF6_PMS= 'GF6_PMS'
    GF6_WFV= 'GF6_WFV'
    GJ1D_PMS= 'GJ1D_PMS'
    GF5_DPC= 'GF5_DPC'
    GF5_VIMS= 'GF5_VIMS'
    GF5_AHSI= 'GF5_AHSI'
    GF5_AIUS= 'GF5_AIUS'
    GF5_GMI= 'GF5_GMI'
    GF5_EMI= 'GF5_EMI'
    GF7_DLC= 'GF7_DLC'
    GF7_BWD= 'GF7_BWD'
    GF7_LSA= 'GF7_LSA'
    CB04_MUX= 'CB04_MUX'
    CB04_P10= 'CB04_P10'
    CB04_P5M= 'CB04_P5M'
    CB04_PM= 'CB04_PM'
    CB04_IRS= 'CB04_IRS'
    CB04_WFI= 'CB04_WFI'
    ZY02C_PMS= 'ZY02C_PMS'
    ZY02C_HRC= 'ZY02C_HRC'
