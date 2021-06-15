import os.path
import re

import pandas as pd
import openpyxl

print(os.getcwd())
print("开始处理DF1数据")

try:
    df = pd.DataFrame(pd.read_excel(r"./DF1.xls"))
except Exception as e:
    df = pd.DataFrame(pd.read_excel(r"./DF1.xlsx"))
    print(e)
except Exception as e:
    print("请在文件目录放置文件名为DF1,后缀为xls或xlsx的数据表")
    print(e)
df.drop(df.index[0])
list_name = list(df)
df=df.fillna(0)
# df=df.dropna(subset=['列名'])

req_data = []

for i in range(len(df)):
    data = {}
    for j in list_name:
        if j == 'Description':#处理Description数据
            if df[j][i]!=0:
               data["Description"] = df[j][i]
        if j == 'Defect Detail':
            if df[j][i]!=0:
               data["Defect Detail"] = str(df[j][i]).splitlines()#处理Defect Detail数据
    req_data.append(data)#获取所需数据到表DF2时提取
while {} in req_data:
    req_data.remove({})


df2=pd.DataFrame.from_dict(req_data)#数据格式转化为df
df2=df2.fillna(0)#数据为空的填充为0

df3=zip(df2.get("Description"),df2.get('Defect Detail'))#zip合并数据
df3=dict(df3)#数据格式转化为字典方便处理

for k,v in list(df3.items()):
    if v==0:
        df3.pop(k)#数据为0的删除

pattern=""
import re
rp = re.compile('\S{9}')
dd4= {}
for k, v in df3.items():
    dd4[k]=[]
    for i in v:
        j = rp.search(i).group()
        dd4[k].append(j)

print(dd4)
df3=dd4

print("开始处理DF2数据")
if os.path.isfile(r"./DF2.xls")==True:#判断文件是否存在并取对应格式
    print("DF2.xls存在")
    df4 = pd.DataFrame(pd.read_excel(r"./DF2.xls"))
elif os.path.isfile(r"./DF2.xlsx")==True:
    print("DF2.xlsx存在")
    df4 = pd.DataFrame(pd.read_excel(r"./DF2.xlsx"))
else:
    print("请在文件目录放置文件名为DF2,后缀为xls或xlsx的数据表")

list_name2=list(df4)

datat = []
datat.append(list_name2)
for k,v in list(df3.items()):#df3循环
    ww=[]
    for w in range(len(list_name2)-1):
        if w==0:
            ww.append(k)
        ww.append(" ")
    datat.append(ww)
    issue_arr =[]
    pv=df4.iloc[:,0].values
    for qq in v:#df4循环
        if qq not in pv:
            dw = []
            for w in range(len(list_name2) - 1):
                if w == 0:
                    dw.append("{} is not found".format(qq))
                dw.append(" ")
            datat.append(dw)
        else:
            for i in range(len(df4)):
                if qq == df4["Issue Num"][i] and str(df4['State'][i])!="Closed":#获取在列表内且状态不为关闭的issue num
                    # print(df4.loc[i])
                    datat.append(df4.loc[i])#根据issue num获取
                    print("")
                    print("添加数据")
                    print(df4.loc[i])


    datat.append(" ")

dft=pd.DataFrame.from_dict(datat)
dft.to_excel("./DF3.xlsx")
while True:
    Q=input("处理完成，输入Q+回车退出程序")
    if Q!="Q":
        Q=input("处理完成，输入Q+回车退出程序")
    else:
        break