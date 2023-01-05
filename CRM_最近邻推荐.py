import pymysql
import numpy as np
import math

conn = pymysql.connect(host="127.0.0.1",
                       port=3306,
                       user='root',
                       passwd='123456789',
                       db='financial_system',
                       charset='utf8')

mid = [] # 作为中间列表将fetchall返回的值转为列表形式
PriceList = []
DetailList = []
result_ID = []
Price_distance = []
Detail_distance = []
Eucidean_distance_group = {} # 定义字典，同时存储最近邻的欧几里得距离与商品的ID
Eucidean_distance_group_sorted = {}
 # 定义全局变量，表示总共的商品个数
cursor = conn.cursor()

def data_switch(): # 数据转换，将fetchall返回的price和idledetails转化为列表形式并返回
  global Num
  sql = "SELECT COUNT(StkCdoTrd) FROM lstkinfo " # 判断数据库中一共有多少种商品类别
  cursor.execute(sql)
  commodityNum = cursor.fetchall()
  a = list(commodityNum[0])
  Num = a[0]
  for i in range(1,Num + 1):
    sql = "SELECT CsrcICNm,CsrcIcNm1 FROM lstkinfo WHERE StkCdoTrd = '%s'" % i # 根据id号返回商品价格和新旧程度
    cursor.execute(sql)
    data = cursor.fetchall()
    try:
      mid.append(list(data[0]))
    except:
      pass
  for i in range(0,Num):
    PriceList.append(float(mid[i][0]))
    DetailList.append(float(mid[i][1]))
  return PriceList,DetailList,Num

def price_distance_function(x): # 计算价格最近邻，x为前端click后返回的商品ID号
  data_switch()
  price_max_difference = max(PriceList) - min(PriceList) # 最大差值
  for item in PriceList:
    m = round(abs((PriceList[x - 1] - item) / price_max_difference),3) # 归一化
    Price_distance.append(m)
  return Price_distance

def detail_distance_function(x): # 计算品相最近邻，x为前端click后返回的商品ID号
  detail_max_difference = max(DetailList) - min(DetailList) # 最大差值
  for item in DetailList:
    n = round(abs((DetailList[x - 1] - item) / detail_max_difference),3) # 归一化
    Detail_distance.append(n)
  return Detail_distance

def sortedDictValues(adict): 
    items = list(adict.items())
    items.sort(key = lambda x:x[1],reverse = False) # 倒序输出，寻找欧几里得距离最小的三个商品ID
    return [[key,value] for key, value in items]

def Cal_Eucidean_distance(x): # 计算欧几里得距离并排序输出N个最近邻商品的ID号
  for i in range(0,Num):
    b = round(math.sqrt(np.square(Price_distance[i]) + np.square(Detail_distance[i])),3)
    
    Eucidean_distance_group[i + 1] = b  # 将所选择的商品与商品库中其余商品的欧几里得距离和各商品ID号放入字典
  result = sortedDictValues(Eucidean_distance_group)

  for i in range(len(result)):
    result_ID.append(result[i][0])
  result_ID.remove(x)
  print(result_ID[:4])

def Eucidean_final():
  price_distance_function(id)
  detail_distance_function(id)
  Cal_Eucidean_distance(id)

# id = input()
id = '000012'
Eucidean_final()

# 关闭游标
cursor.close()

# 关闭链接
conn.close()




