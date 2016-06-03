#coding:utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.

# 用户表
class UserTable(models.Model):
	UserID = models.CharField(max_length=20)
	Name = models.CharField(max_length=20)
	IDcard = models.CharField(max_length=20)
	Gender = models.IntegerField()
	Occupation = models.CharField(max_length=20)
	EduInfo = models.CharField(max_length=20)
	HomeAddr = models.TextField()
	Department = models.TextField()
	Tel = models.CharField(max_length=20)
	MailAddr = models.CharField(max_length=20)
	Age = models.IntegerField()

# 证券账户基本信息
class SecurityAccountInfo(models.Model):
	SecurityID = models.CharField(max_length=20)

# 资金账户基本信息
class CapitalAccountInfo(models.Model):
	AccountID = models.CharField(max_length=20)
	Password = models.CharField(max_length=20)
	Isfirst = models.BooleanField(default=1)
	UserTable = models.ForeignKey(UserTable)
	BuyPassword = models.CharField(max_length=20)
	SecurityAccount = models.ForeignKey(SecurityAccountInfo)
	loginPwdWrongNum = models.IntegerField(default=0)
	transPwdWrongNum = models.IntegerField(default=0)
	lastTimeTrans = models.DateTimeField()
	lastTimeLogin = models.DateTimeField()
	IsTransFreeze = models.BooleanField()
	IsLoginFreeze = models.BooleanField()

class InstDealed(models.Model): #the table of Dealed Instructions
	InstID = models.CharField(max_length=20)
	TimeSubmit = models.DateTimeField()
	TimeDealed = models.DateTimeField()
	InstType = models.IntegerField() # buy/sell
	StockID = models.CharField(max_length=20)
	AccountID = models.ForeignKey(CapitalAccountInfo)
	SecurityID = models.ForeignKey(SecurityAccountInfo)
	Quantity = models.IntegerField()
	PriceSubmit = models.FloatField() #submit price
	PriceDealed = models.FloatField() #dealed price

class InstOutOfDate(models.Model): #the table of Dealed Instructions
	InstID = models.CharField(max_length=20)
	TimeSubmit = models.DateTimeField()#submit time
	TimeOutOfDate = models.DateTimeField() #out of date time
	InstType = models.IntegerField() # buy/sell
	StockID = models.CharField(max_length=20) 
	AccountID = models.ForeignKey(CapitalAccountInfo)
	SecurityID = models.ForeignKey(SecurityAccountInfo)
	Quantity = models.IntegerField()
	PriceSubmit = models.FloatField() #submit price

# 资金信息
class CapitalInfo(models.Model):
	AccountID = models.CharField(max_length=20)
	ActiveMoney = models.FloatField()
	FrozenMoney = models.FloatField()
	BankCard = models.CharField(max_length=20)

# 证券账户持有股票信息
class SecurityStockInfo(models.Model):
	SecurityID = models.CharField(max_length=20)
	StockID = models.CharField(max_length=20)
	ShareHolding = models.IntegerField()	#股数
	status = models.IntegerField()
	BuyPrice = models.FloatField()
