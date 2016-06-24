#!/usr/bin/env python2.7 
import sys;
import os;

# NOTE: PLEASE comment or edit this line if you want to test the module yourself
sys.path.append('C:/users/shorc/documents/github/stock_trading_system/');


# environment stuff
from django.apps import apps;
from django.conf import settings;
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Stock_Trading_System.settings");
from django.core.management import execute_from_command_line;
execute_from_command_line(sys.argv);
# ~~env

# database dependence
from database.models import *;

# in-module dependence
from globalvar import GlobalVar;
from priorityQueue import PriorityQueue;

glob = GlobalVar();
instIdCount = 0;


def init_central_trading_system():
	stockInfoList = StockInfo.objects.all();
	securityStockInfoList = SecurityStockInfo.objects.all();	# this is accounts!!!
	
	for iStock in stockInfoList:
		glob.InstQueue[iStock.StockID] = (PriorityQueue(),PriorityQueue());
	
	for iAccount in securityStockInfoList:	# iSecStock
		glob.InstNotDealt[iAccount.SecurityID] = {};

	return True;

def buy(inst):
	inst[0] = instIdCount;
	instIdCount += 1;
	instTp = inst[2];	# instType
	assert (instTp == 0);

	glob.match(inst);

def sell(inst):
	inst[0] = instIdCount;
	instIdCount += 1;
	instTp = inst[2];
	assert (instTp == 1);

	glob.match(inst);

def query(securityId):
	return glob.InstNotDealt[securityId];

def admin_query():
	return glob.InstNotDealt;

def revoke(instId):
	glob.delete(instId);

#inst = (ID,time,type,StockID,securityID,accountID,quantity,price) 
#		[0] [1]  [2]  [3]		[4]			 [5]	   [6]	  [7]

inst=('0000002','201606071945',0,'0001','3130102347','123',400,124.32);
sellI=('0000003','201606071946',1,'0001','3130102345','124',100,124.32);
glob.InstQueue['0001'] = (PriorityQueue(),PriorityQueue());
glob.insert(inst);
# sell(sellI); ! CAN'T DO this because the tables are empty
print query('3130102347');

