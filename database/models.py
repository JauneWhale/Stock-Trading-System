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
	MailAddr = models.CharField(max_length=30)
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

#成交指令表
class InstDealed(models.Model): 
	InstID = models.CharField(max_length=20)
	TimeSubmit = models.DateTimeField() #提交时间
	TimeDealed = models.DateTimeField() #成交时间
	InstType = models.IntegerField() # 买/卖
	StockID = models.CharField(max_length=20)
	AccountID = models.ForeignKey(CapitalAccountInfo)
	SecurityID = models.ForeignKey(SecurityAccountInfo)
	Quantity = models.IntegerField()
	PriceSubmit = models.FloatField() # 提交价格
	PriceDealed = models.FloatField() # 成交价格

#未成交指令表
class InstNotDealed(models.Model): 
	InstID = models.CharField(max_length=20)
	TimeSubmit = models.DateTimeField() # 提交时间
	TimeOutOfDate = models.DateTimeField() #过期时间
	InstType = models.IntegerField() # 买/卖
	InstState = models.IntegerField() # 过期/撤销
	StockID = models.CharField(max_length=20) 
	AccountID = models.ForeignKey(CapitalAccountInfo)
	SecurityID = models.ForeignKey(SecurityAccountInfo)
	Quantity = models.IntegerField() # 股票数量
	PriceSubmit = models.FloatField() # 提交价格
# 股票信息
class StockInfo(models.Model):
	StockName = models.TextField()
	StockID = models.CharField(max_length=20) 
	CurrentPrice = models.FloatField() # 当前价
	MaxPrice = models.FloatField() # 当日最高价
	MinPrice = models.FloatField() # 当日最低价
	TodayOpeningPrice = models.FloatField() # 今开
	YesterdayClosingPrice = models.FloatField() # 昨收
	Quantity = models.IntegerField() # 数量
	UpLimit = models.FloatField() # 涨幅
	BottomLimit = models.FloatField() # 跌幅
	

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
