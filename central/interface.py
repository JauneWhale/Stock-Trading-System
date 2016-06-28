#!/usr/bin/env python2.7 
import sys;
import os;

# NOTE: PLEASE comment or edit this line if you want to test the module yourself
# sys.path.append('C:/users/shorc/documents/github/stock_trading_system/');
#sys.path.append('/home/jj/gitProject/sst2/Stock_Trading_System');

# environment stuff
from django.apps import apps;
from django.conf import settings;
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Stock_Trading_System.settings");
from django.core.management import execute_from_command_line;
#execute_from_command_line(sys.argv);
# ~~env

# database dependence
from database.models import *;

# in-module dependence
import globalvar;
from priorityQueue import PriorityQueue;


def init_central_trading_system():
	glob = globalvar.GlobalVar();
	stockInfoList = StockInfo.objects.all();
	securityStockInfoList = SecurityStockInfo.objects.all();	# this is accounts!!!
	
	for iStock in stockInfoList:
		glob.InstQueue[iStock.StockID] = (PriorityQueue(),PriorityQueue());
	
	for iAccount in securityStockInfoList:	# iSecStock
		glob.InstNotDealt[iAccount.SecurityID] = {};

	return True;

def buy(inst):
	glob = globalvar.GlobalVar();
	# inst[0] = glob.instIdCount;
	inst_new = (str(glob.instIdCount),inst[1],inst[2],inst[3],inst[4],inst[5],inst[6],inst[7]);
	glob.instIdCount += 1;
	instTp = inst[2];	# instType
	assert (instTp == 0);

	print inst_new
	
	glob.match(inst_new);

def sell(inst):
	glob = globalvar.GlobalVar();
	# inst[0] = glob.instIdCount;
	inst_new = (str(glob.instIdCount),inst[1],inst[2],inst[3],inst[4],inst[5],inst[6],inst[7]);
	glob.instIdCount += 1;
	instTp = inst[2];
	assert (instTp == 1);

	print inst_new

	glob.match(inst_new);

def query(securityId):
	glob = globalvar.GlobalVar();
	return glob.InstNotDealt[securityId];

def admin_query():
	glob = globalvar.GlobalVar();
	Stocklist = {};
	buy_list=[];
	sell_list=[];
	for account in glob.InstNotDealt:
		for inst in glob.InstNotDealt[account]:
			_inst = glob.InstNotDealt[account][inst];
			if(_inst[2] == 0): #buy
				buy_list.append({"id":_inst[0],"p_id":_inst[4],"price":_inst[7],"amount":_inst[6]});	
			elif(_inst[2]==1): #sell
				sell_list.append({"id":_inst[0],"s_id":_inst[4],"price":_inst[7],"amount":_inst[6]});
	Stocklist={"buy_list":buy_list,"sell_list":sell_list};
	return Stocklist;

def revoke(instId):
	glob = globalvar.GlobalVar();
	glob.delete(instId);

def renew(stockId):
	stockInfo = StockInfo.objects.get(StockID=stockId);
	stockInfo.state=0;
	
def froze(stockId):
	glob = globalvar.GlobalVar();
	stockInfo = StockInfo.objects.get(StockID=stockId);
	stockInfo.state=1;
	glob.flush(stockId); #clear the InstNotDealt map and the queue, push them into the database


#inst = (ID,time,type,StockID,securityID,accountID,quantity,price) 
#		[0] [1]  [2]  [3]		[4]			 [5]	   [6]	  [7]

# inst=('0000002','201606071945',0,'0001','3130102347','123',400,124.32);
# inst2=('0000004','201606071945',0,'0001','3130102346','123',400,124.32);
# inst3=('0000005','201606071945',1,'0001','3130102234','123',400,124.32);
# sellI=('0000003','201606071946',1,'0001','3130102345','124',100,124.32);
# #glob.InstQueue['0001'] = (PriorityQueue(),PriorityQueue());
# #glob.insert(inst);
# #glob.insert(inst2);
# #glob.insert(inst3);
# # sell(sellI); ! CAN'T DO this because the tables are empty
# print query('3130102347');
# print admin_query();

