ModisDownload
-------------

help ours down load from base url
https://ladsweb.modaps.eosdis.nasa.gov/ when i use this packages , our
bandwidth work in deadline with the first version we can use this
download all modis file with any time in any area use like this

.. code:: python

   search_p()
   search_area()
   reload()
   g=getHtml("your token")
   g.download_main("production name","time,time1..time2","area or x1y1,x1y1","download dir")

SearchChinaData
---------------

it also can get metadata about `china image
search_area <http://36.112.130.153:7777/#/mapSearch>`__

use this kind command

.. code:: python

   from ModisDownload.InitCHN import Init
   from ModisDownload.PolygonUtiles import Poly
   from ModisDownload.SearchCHN import SearchData,SearchChina
   from ModisDownload.Base import Sensors
   from ModisDownload import visited

   def searchChinaExample():
       Init(False)
       geom = Poly.Point(123.1231, 34.123)
       geom2 = Poly.Polygon(
           [[105.550278, 32.174096], [105.550278, 28.707072], 
            [109.525337, 28.707072], [109.525337, 32.174096]])
       geom3 = Poly.Square(104.550278, 28.174096, 109.525337, 18.707072)
       searchData = SearchData("2021-05-11", "2022-05-21",
                               [Sensors.GF1B_PMS, Sensors.LT1B_SAR, Sensors.GF4_B3,
                                Sensors.ZY302_NAD, Sensors.GF5_EMI, Sensors.CSES_GRO]
                               , [geom, geom2, geom3], 60, 1)
       search = SearchChina(searchData, True)
       search.search()
       search.save_ans("ans.csv")
       return

   if __name__ == '__main__':
       searchChinaExample()
