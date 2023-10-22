## ModisDownload
help ours down load from base url https://ladsweb.modaps.eosdis.nasa.gov/
when i use this packages , our bandwidth work in deadline
with the first version we can use this download all modis file with any time in any area
use like this
```python
reload()
g=getHtml("your token")
g.download_main("production name","time,time1..time2","area or x1y1,x1y1","download dir")
```
