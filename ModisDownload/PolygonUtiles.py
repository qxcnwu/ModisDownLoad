# -*- coding: utf-8 -*-
# @Time    : 2022/5/21 22:20
# @Author  : qxcnwu
# @FileName: PolygonUtiles.py
# @Software: PyCharm

class Poly:
    def __init__(self):
        pass

    @staticmethod
    def Polygon(points:list)->str:
        """
        多个点集合
        Args:
            points:

        Returns:

        """
        temp="POLYGON(("
        for x,y in points:
            temp=temp+str(x)+" "+str(y)+","
        temp=temp+str(points[0][0])+" "+str(points[0][1])+"))"
        return temp

    @staticmethod
    def Point(lon:float,lat:float)->str:
        """
        单个点
        Args:
            lon:经度
            lat: 纬度
        Returns:
        """
        return "POINT("+str(lon)+" "+str(lat)+")"

    @staticmethod
    def Square(lon:float,lat:float,lon_:float,lat_:float)->str:
        """
        两个角点经纬度决定矩形
        Args:
            lon: 左上角经度
            lat: 左上角为度
            lon_: 右下角经度
            lat_: 右下角纬度
        Returns:

        """
        return Poly.Polygon([[lon,lat],[lon,lat_],[lon_,lat_],[lon_,lat]])