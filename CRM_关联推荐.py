from itertools import combinations
import sys
from PyQt5 import uic
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import *
from PyQt5 import QtSql

db = QtSql.QSqlDatabase.addDatabase("QODBC");
db.setHostName("localhost");
db.setDatabaseName("crm");
db.setUserName("sa");
db.setPassword("123456");
if (db.open()):
    print('Opened Successfully！')

min_support = 0.1 # 最小支持度为30%
min_related = 0.5 # 最小相关度为50%
min_interested = 1 # 兴趣度为1

commodityPiece = [] # 商品种类
purchase = [] # 商品购买记录
one_set_name = [] # 单一商品频繁项目集(名称) 方便测试使用
one_set_support = [] # 单一商品频繁项目集(支持度) 方便测试使用
two_set_name = [] # 二元商品频繁项目集(名称) 方便测试使用
two_set_support = [] # 二元商品频繁项目集(支持度) 方便测试使用

one_set = [] # 单一商品频繁项目集
two_set = [] # 二元商品频繁项目集

interested_recommended_commodity = []
believed_recommended_commodity = []

def commodity_piece():   # 查询所有购买信息中一共含有几种类型的商品
  query0 = QSqlQuery()
  sql = "select distinct commodityName from boughtlist"
  query0.exec(sql)
  while(query0.next()):
    commodityPiece.append(query0.value(0))
  return commodityPiece

def find_Num():  # 查询所有购买信息中一共有多少位用户
  query0 = QSqlQuery()
  sql = "SELECT COUNT(DISTINCT custormerNo) FROM boughtlist"
  query0.exec(sql)
  query0.next()
  return query0.value(0)

def find_one(x): # 查询单一商品所有的购买记录
  purchase = [] # 每次调用函数前需要清空列表
  query0 = QSqlQuery()
  sql = "select custormerNo from boughtlist where commodityName = '%s'" % (x)
  query0.exec(sql)
  while(query0.next()):
    purchase.append(query0.value(0))
  return purchase

def find_two(x,y): # 查询单一商品频繁集中的二元子集商品所有的购买记录
  purchase = [] # 每次调用函数前需要清空列表
  query0 = QSqlQuery()
  sql = "select custormerNo from boughtlist where commodityName in ('%s','%s') and custormerNo in ( select custormerNo from boughtlist where commodityName = '%s' and custormerNo in (select custormerNo from boughtlist where commodityName = '%s'))" % (x,y,x,y)
  query0.exec(sql)
  while(query0.next()):
    purchase.append(query0.value(0))
  return purchase

def support_degree_one(x): # 计算单一商品的支持度
  a = len(find_one(x)) / find_Num()
  if a > min_support:
    one_set_name.append(x) # 商品名称输入one_set_name
    one_set_support.append(a) # 商品支持度输入one_set_support
    one_set.append(x) # 商品名称输入one_set
    one_set.append(a) # 商品支持度输入one_set
  return one_set_support,one_set_name

def support_degree_two(i,j): # 计算二元相关商品的支持度
  b = len(find_two(i,j)) / find_Num() * 0.5
  if b > min_support:
    two_set_name.append([i,j]) # 商品名称输入two_set_name
    two_set_support.append(b) # 商品支持度输入two_set_support
    two_set.append([i,j]) # 商品名称输入two_set
    two_set.append(b) # 商品支持度输入two_set
    two_set.append([j,i]) # 真是给我机灵坏了
    two_set.append(b) 
  return two_set_support,two_set_name

def believed_degree(x): # 置信度计算函数
  one_set_name_repeat = one_set_name
  if x in one_set_name:
    one_set_name_repeat.remove(x)
  for i in range(len(one_set_name_repeat)):
   if len(find_two(x,one_set_name_repeat[i])) / find_Num() != 0:
      c = two_set.index([x,one_set_name_repeat[i]]) + 1 # 定位二元组合的下一个元素即为该组合的支持度
      related_degree = two_set[c] / one_set[one_set.index(x) + 1]
      if related_degree > min_related:
        believed_recommended_commodity.append(one_set_name_repeat[i])
        print('the related degree of {A} to {B} is:'.format(A = x,B = one_set_name_repeat[i]))
        print(related_degree)
  one_set_name.append(x)
  return believed_recommended_commodity
  
def interested_degree(x): # 兴趣度计算函数
  one_set_name_repeat = one_set_name
  if x in one_set_name:
    one_set_name_repeat.remove(x)

  for i in range(len(one_set_name_repeat)):
    if len(find_two(x,one_set_name_repeat[i])) / find_Num() != 0:
   
      d = two_set.index([x,one_set_name_repeat[i]]) + 1 # 定位二元组合的下一个元素即为该组合的支持度
      n = two_set[d]
      m = float(one_set[one_set.index(one_set_name_repeat[i]) + 1])
      p = float(one_set[one_set.index(x) + 1])
      interested_degree = n / (m * p)
      if interested_degree > min_interested: 
        interested_recommended_commodity.append(one_set_name_repeat[i])
        print('the interested degree of {A} to {B} is:'.format(A = x,B = one_set_name_repeat[i]))
        print(interested_degree)
  one_set_name.append(x)
  return interested_recommended_commodity

def final_fun():
  commodity_piece() 
  for x in commodityPiece:
    support_degree_one(x)
  two_plan = list(combinations(one_set_name,2)) # 一元频繁商品集中取二元组合
  for i,j in two_plan:
    support_degree_two(i,j)

x = '数据结构'
final_fun()
# print('一元频繁集',one_set)
# print('一元频繁集名称',one_set_name)
# print('一元频繁集支持度',one_set_support)
# print('二元频繁集',two_set)
# print('二元频繁集名称',two_set_name)
# print('二元频繁集支持度',two_set_support)
believed_degree(x)
print('根据置信度推荐的商品集有：',believed_recommended_commodity)
# print(believed_recommended_commodity)
interested_degree(x)
print('根据兴趣度推荐的商品集有：',interested_recommended_commodity)
# print(interested_recommended_commodity)