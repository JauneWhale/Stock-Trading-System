#!/usr/bin/env python2.7 
import globalvar
import priorityQueue
from database.models import StockInfo
from database.models import SecurityStockInfo

def init_globalvar():
	aa = globalvar.GlobalVar()
	stockInfoList = StockInfo.objects.all()
	securityStockInfoList = SecurityStockInfo.objects.all()
	
	for i in stockInfoList:
		items = [(0,priorityQueue.PriorityQueue()),(1,priorityQueue.PriorityQueue())]
		second_dict = dict(items)
		aa.InstQueue[i.StockID] = second_dict
	
	for j in securityStockInfoList:
		aa.InstNotDealt[j.SecurityID] = []
	print aa.InstQueue
	print aa.InstNotDealt
	
	return aa
def buy(inst):
	aa = GlobalVar()
	if(inst[2]<>0):
		return False
	else:
		sellQueue = aa.InstQueue[inst[3]][1].queue
		if(inst[7]<sellQueue[0][0]):
			insert(inst)
			return True
		else:
			frontSellInst = sellQueue[0][1]
			remain = inst[6]
			while(remain>=frontSellInst[6] and inst[7]>=frontSellInst[7]):
				sellQueue.get()
				
				####	database operations here
			
				remain = remain - frontSellInst[6]
				frontSellInst = sellQueue[0][1]
			if(inst[7]<frontSellInst[7]):
				####	insert back
				return True	
