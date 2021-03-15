# -*- coding: utf-8 -*-
#author:Ryan
#time  :2021/3/14
import requests,json
from lxml import etree


header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"}

url="https://www.xicidaili.com/nn/"

res=requests.get(url=url,headers=header)
res.encoding="utf-8"

if res.status_code == 200:
	html=etree.HTML(res.text)
	table=html.xpath("//tabler[@id=ip_list]")[0]
	trs=table.xpath("//tr")[1:]
arr=[]
for i in trs:
	ip=i.xpath("td/text()")[0]
	port=i.xpath("td/text()")[1]
	arr["ip"]=ip
	arr["port"]=port
print(arr)