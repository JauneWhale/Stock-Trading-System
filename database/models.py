#coding:utf-8
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.

# 用户表
class UserTable(models.Model):
	UserID = models.CharField(max_length=20)
	Name = models.CharField(max_length=20)
	IDcard = models.CharField(max_length=20,default='0')
	Gender = models.IntegerField(default=0)
	Occupation = models.CharField(max_length=20,default='0')
	EduInfo = models.CharField(max_length=20,default='0')
	HomeAddr = models.TextField(default='0')
	Department = models.TextField(default='0')
	Tel = models.CharField(max_length=20,default='0')
	MailAddr = models.CharField(max_length=30,default='0')
	Age = models.IntegerField(default='0')

# 证券账户基本信息
class SecurityAccountInfo(models.Model):
	SecurityID = models.CharField(max_length=20)

# 资金账户基本信息
class CapitalAccountInfo(models.Model):
	AccountID = models.CharField(max_length=20)
	Password = models.CharField(max_length=20,default='0')
	Isfirst = models.BooleanField(default=1)
	UserTable = models.ForeignKey(UserTable)
	BuyPassword = models.CharField(max_length=20,default='0')
	SecurityAccount = models.ForeignKey(SecurityAccountInfo)
	loginPwdWrongNum = models.IntegerField(default=0)
	transPwdWrongNum = models.IntegerField(default=0)
	lastTimeTrans = models.DateTimeField(default=timezone.now())
	lastTimeLogin = models.DateTimeField(default=timezone.now())
	IsTransFreeze = models.BooleanField(default=0)
	IsLoginFreeze = models.BooleanField(default=0)

#成交指令表
class InstDealed(models.Model): 
	InstID = models.CharField(max_length=20)
	TimeSubmit = models.DateTimeField(default=timezone.now()) #提交时间
	TimeDealed = models.DateTimeField(default=timezone.now()) #成交时间
	InstType = models.IntegerField(default=0) # 买/卖
	StockID = models.CharField(max_length=20)
	AccountID = models.ForeignKey(CapitalAccountInfo)
	SecurityID = models.ForeignKey(SecurityAccountInfo)
	Quantity = models.IntegerField(default=1)
	PriceSubmit = models.FloatField(default=0) # 提交价格
	PriceDealed = models.FloatField(default=0) # 成交价格

#未成交指令表
class InstNotDealed(models.Model): 
	InstID = models.CharField(max_length=20)
	TimeSubmit = models.DateTimeField(default=timezone.now()) # 提交时间
	TimeOutOfDate = models.DateTimeField(default=timezone.now()) # 过期时间
	InstType = models.IntegerField(default=0) # 买/卖
	InstState = models.IntegerField(default=0) # 过期/撤销
	StockID = models.CharField(max_length=20) 
	AccountID = models.ForeignKey(CapitalAccountInfo)
	SecurityID = models.ForeignKey(SecurityAccountInfo)
	Quantity = models.IntegerField(default=1) # 股票数量
	PriceSubmit = models.FloatField(default=0) # 提交价格

# 股票信息
class StockInfo(models.Model):
	StockName = models.TextField()
	StockID = models.CharField(max_length=20) 
	CurrentPrice = models.FloatField(default=0) # 当前价
	MaxPrice = models.FloatField(default=0) # 当日最高价
	MinPrice = models.FloatField(default=0) # 当日最低价
	TodayOpeningPrice = models.FloatField(default=0) # 今开
	YesterdayClosingPrice = models.FloatField(default=0) # 昨收
	Quantity = models.IntegerField(default=0) # 数量
	UpLimit = models.FloatField(default=0) # 涨幅
	BottomLimit = models.FloatField(default=0) # 跌幅
	State = models.BooleanField(default=0) #1:Frozen 0:OK
	

# 资金信息
class CapitalInfo(models.Model):
	AccountID = models.CharField(max_length=20,)
	ActiveMoney = models.FloatField(default=0)
	FrozenMoney = models.FloatField(default=0)
	BankCard = models.CharField(max_length=20,default='0')

# 证券账户持有股票信息
class SecurityStockInfo(models.Model):
	SecurityID = models.CharField(max_length=20)
	StockID = models.CharField(max_length=20)
	ShareHolding = models.IntegerField(default=0)	#股数
	status = models.IntegerField(default=0)
	BuyPrice = models.FloatField(default=0)

# 管理员管理股票列表
class StockManage(models.Model):
    AdminID = models.ForeignKey(UserTable, related_name="admin")
    StockID = models.ForeignKey(StockInfo, related_name="stock")
