#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
import interface
import globalvar
# Create your views here.
def initial(request):
	interface.init_globalvar();
	return HttpResponse("欢迎光临 自强学堂!")

def insert(request):
	#inst = (ID,time,type,StockID,securityID,accountID,quantity,price) 
	#	[0] [1]  [2]  [3]	[4]	[5]	 [6]	 [7]
	inst = {0:('0000001','201606071939',0,'0001','3130102346','110',300,123.32)}	
	
	inst[1]=('0000002','201606071945',0,'0001','3130102347','123',400,124.32)
	inst[2]=('0000003','201606071955',1,'0001','3130102356','120',500,124.32)
	inst[3]=('0000004','201606072039',1,'0002','3130102367','120',1000,88.32)
	
	aa = globalvar.GlobalVar()
	for i in range(4):
		print ("instget"),
		print inst[i]
		print ("insert into stock"+inst[i][3])
		aa.insert(inst[i])
		bb = aa.InstQueue[inst[i][3]][0].queue
		cc = aa.InstQueue[inst[i][3]][1].queue
		if inst[i][2] is 0:
			print ("the first element in the buy queue:"+bb[0][1][0])
		else:		
			print ("the first element in the sell queue:"+cc[0][1][0])
	print ("Instruction not dealt"),
	print aa.InstNotDealt
	return HttpResponse()
	

