#coding:utf-8
#!/usr/bin/env python2.7 
import priorityQueue;
from database.models import *;
import datetime;

import pdb;

class GlobalVar(object): 
	# self.InstQueue = {};			# stockId -> (buyPq, sellPq)
	# self.InstNotDealt = {};		# usrId -> instMap[instId]

	def __init__(self):
		self.InstQueue = {};
		self.InstNotDealt = {};
		self.instIdCount = 0

	def insert_notDealt(self, inst):
		if( self.InstNotDealt.has_key( inst[4] ) ):
			self.InstNotDealt[ inst[4] ][ inst[0] ] = list(inst);
		else:
			self.InstNotDealt[inst[4]]={};
			self.InstNotDealt[ inst[4] ][ inst[0] ] = list(inst);

	def match(self, inst):

		inst = list(inst);
		# pdb.set_trace();
		print self.InstQueue
		if ( self.InstQueue.has_key( inst[3] ) ):
			if ( inst[2] == 0 ):
				toMatchQueue = self.InstQueue[ inst[3] ][1];
			else:
				toMatchQueue = self.InstQueue[ inst[3] ][0];
			
			while ( (not toMatchQueue.empty()) and inst[6] > 0):	# try to match
				toMatch = toMatchQueue.peek();
				print toMatch;
				# pdb.set_trace();
				if ( (toMatch[2] == 0 and toMatch[7] < inst[7]) or
					 (toMatch[2] == 1 and toMatch[7] > inst[7]) ):
					break;

				dealPrice = (toMatch[7] + inst[7]) / 2;
				dealTime = datetime.datetime.now();
				stockNewPrice = dealPrice;	# temporary
				dealQuantity = inst[6];

				if ( toMatch[6] > inst[6] ):	# partial match (quantity)
					
					# stock up limits check is not here
					dealQuantity = inst[6];

					toMatch[6] -= dealQuantity;
					inst[6] = 0;

					# update instNotDealt map
					self.InstNotDealt[ toMatch[4] ][ toMatch[0] ][6] = toMatch;
					# update toMatchQueue
					toMatchQueue.update(toMatch, 0);

				elif ( toMatch[6] < inst[6] ):

					dealQuantity = toMatch[6];

					inst[6] -= dealQuantity;

					# update instNotDealt map
					self.InstNotDealt[ toMatch[4] ].pop( toMatch[0] );
					# pop toMatchQueue
					toMatchQueue.get();
				else:

					dealQuantity = inst[6];
					inst[6] -= dealQuantity;
					self.InstNotDealt[ toMatch[4] ].pop( toMatch[0] );
					toMatchQueue.get();

				# update stock price
				stockObj = StockInfo.objects.get(StockID=inst[3]);
				stockObj.CurrentPrice = stockNewPrice;
				stockObj.save();

				if ( inst[2] == 0 ):
					# update buyer account money
					capitalObj = CapitalInfo.objects.get(AccountID=inst[5]);
					capitalObj.ActiveMoney -= dealPrice * dealQuantity;
					capitalObj.save();

					# update seller account money
					capitalObj = CapitalInfo.objects.get(AccountID=toMatch[5]);
					capitalObj.ActiveMoney += dealPrice * dealQuantity;
					capitalObj.save();

					# update buyer shareHolding
					if len(SecurityStockInfo.objects.filter(SecurityID=inst[4], StockID=inst[3])) != 0:
						secInfo = SecurityStockInfo.objects.get(SecurityID=inst[4], StockID=inst[3]); 						
						secInfo.ShareHolding += dealQuantity; 						
						secInfo.save();
					else:
						SecurityStockInfo.objects.create(
						SecurityID = inst[4],
						StockID=inst[3],
						ShareHolding=dealQuantity,
						status=inst[2],
						BuyPrice = inst[7]);

					# update seller shareHolding
					secInfo = SecurityStockInfo.objects.get(SecurityID=toMatch[4], StockID=toMatch[3]);
					secInfo.ShareHolding -= dealQuantity;
					secInfo.save();
				elif ( inst[2] == 1 ):
					# update seller account money
					capitalObj = CapitalInfo.objects.get(AccountID=inst[5]);
					capitalObj.ActiveMoney += dealPrice * dealQuantity;
					capitalObj.save();

					# update buyer account money
					capitalObj = CapitalInfo.objects.get(AccountID=toMatch[5]);
					capitalObj.ActiveMoney -= dealPrice * dealQuantity;
					capitalObj.save();

					# update seller shareHolding
					secInfo = SecurityStockInfo.objects.get(SecurityID=inst[4], StockID=inst[3]);
					secInfo.ShareHolding -= dealQuantity;
					secInfo.save();

					# update buyer shareHolding
					secInfo = SecurityStockInfo.objects.get(SecurityID=toMatch[4], StockID=toMatch[3]);
					secInfo.ShareHolding += dealQuantity;
					secInfo.save();

				# insert 2 insts into dealed instruction table
				InstDealed.objects.create(
					InstID=inst[0],
					TimeSubmit=inst[1],
					TimeDealed=dealTime,
					InstType=inst[2],
					StockID=inst[3],
					AccountID=CapitalAccountInfo.objects.get(AccountID=inst[5]),
					SecurityID=SecurityAccountInfo.objects.get(SecurityID=inst[4]),
					Quantity=dealQuantity,
					PriceSubmit=inst[7],
					PriceDealed=dealPrice
				);
				InstDealed.objects.create(
					InstID=toMatch[0],
					TimeSubmit=toMatch[1],
					TimeDealed=dealTime,
					InstType=toMatch[2],
					StockID=toMatch[3],
					AccountID=CapitalAccountInfo.objects.get(AccountID=toMatch[5]),
					SecurityID=SecurityAccountInfo.objects.get(SecurityID=toMatch[4]),
					Quantity=dealQuantity,
					PriceSubmit=toMatch[7],
					PriceDealed=dealPrice
				);

			# : while

			if inst[6] > 0:	# match failed
				self.insert(inst);
		else:
			print 'false'
			# assert False;

	def insert(self, inst):		# insert an inst into the queue
		#inst = (ID,time,type,StockID,securityID,accountID,quantity,price) 
		#		[0] [1]  [2]  [3]		[4]			 [5]	   [6]	  [7]
		if( self.InstQueue.has_key(inst[3]) ):
			
			if(inst[2]==0):				#type0==buy 队首是最高买价
				self.InstQueue[ inst[3] ][0].put_h2l( (inst, inst[7]) );
				self.insert_notDealt(inst);

			elif(inst[2]==1):			#type1==sell 队首是最低卖价
				self.InstQueue[ inst[3] ][1].put_l2h( (inst, inst[7]) );
				self.insert_notDealt(inst);

			else:
				assert False # not buy or sell
		else:
			assert False # no such stock

	def delete(self, instId):

		inst = self.InstNotDealt[ inst[4] ].pop( inst[0] );
		self.InstQueue.remove(instId);

