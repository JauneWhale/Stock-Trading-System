#!/usr/bin/env python2.7 
import sys
import os

# NOTE: PLEASE comment or edit this line if you want to test the module yourself
# sys.path.append('C:/users/shorc/documents/github/stock_trading_system/')
#sys.path.append('/home/jj/gitProject/sst2/Stock_Trading_System')

# environment stuff
from django.apps import apps
from django.conf import settings
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Stock_Trading_System.settings")
from django.core.management import execute_from_command_line
#execute_from_command_line(sys.argv)
# ~~env

# database dependence
from database.models import *

# in-module dependence
import globalvar
from priorityQueue import PriorityQueue

glob = globalvar.GlobalVar()
instIdCount = 0

def init_central_trading_system():
	global glob

	stockInfoList = StockInfo.objects.all()
	securityStockInfoList = SecurityStockInfo.objects.all()	# this is accounts!!!
	
	for iStock in stockInfoList:
		glob.InstQueue[iStock.StockID] = (PriorityQueue(),PriorityQueue())
	
	for iAccount in securityStockInfoList:	# iSecStock
		glob.InstNotDealt[iAccount.SecurityID] = {}

	return True

def buy(inst):
	global glob
	global instIdCount
	# inst[0] = glob.instIdCount
	inst_new = (str(instIdCount),inst[1],inst[2],inst[3],inst[4],inst[5],inst[6],inst[7])
	instIdCount += 1
	instTp = inst[2]	# instType
	assert (instTp == 0)

	# print inst_new
	
	glob.match(inst_new)

def sell(inst):
	global glob
	global instIdCount
	# inst[0] = glob.instIdCount
	inst_new = (str(instIdCount),inst[1],inst[2],inst[3],inst[4],inst[5],inst[6],inst[7])
	instIdCount += 1
	instTp = inst[2]
	assert (instTp == 1)

	# print inst_new

	glob.match(inst_new)

def query(securityId):
	global glob
	print glob.InstNotDealt
	if glob.InstNotDealt.has_key(securityId):
		return glob.InstNotDealt[securityId]
	else:
		return {}

def admin_query(stockId):
    global glob
    Stocklist = {}
    buy_list=[]
    sell_list=[]

    buy_queue = glob.InstQueue[stockId][0]
    sell_queue = glob.InstQueue[stockId][1]
    for i in range (0,buy_queue.qsize()):
        buy_list.append(buy_queue.queue[i][1])
    for j in range (0,sell_queue.qsize()):
        sell_list.append(sell_queue.queue[j][1])
    Stocklist={"buy_list":buy_list,"sell_list":sell_list}
    return Stocklist

def revoke(instId, s_id):
	global glob
	glob.delete(instId, s_id)

def renew(stockId):
	stockInfo = StockInfo.objects.get(StockID=stockId)
	stockInfo.state=0
	
def froze(stockId):
	global glob
	stockInfo = StockInfo.objects.get(StockID=stockId)
	stockInfo.state=1
	#glob.flush(stockId) #clear the InstNotDealt map and the queue, push them into the database

init_central_trading_system()

#inst = (ID,time,type,StockID,securityID,accountID,quantity,price) 
#		[0] [1]  [2]  [3]		[4]			 [5]	   [6]	  [7]

# inst=('0000002','201606071945',0,'0001','3130102347','123',400,124.32)
# inst2=('0000004','201606071945',0,'0001','3130102346','123',400,124.32)
# inst3=('0000005','201606071945',1,'0001','3130102234','123',400,124.32)
# sellI=('0000003','201606071946',1,'0001','3130102345','124',100,124.32)
# #glob.InstQueue['0001'] = (PriorityQueue(),PriorityQueue())
# #glob.insert(inst)
# #glob.insert(inst2)
# #glob.insert(inst3)
# # sell(sellI) ! CAN'T DO this because the tables are empty
# print query('3130102347')
# print admin_query()

