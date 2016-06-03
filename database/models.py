#coding:utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class UserTable(models.Model):
	UserID = models.CharField()
	Name = models.CharField()
	IDcard = models.CharField()
	Gender = models.IntegerField()
	Occupation = models.CharField()
	EduInfo = models.CharField()
	HomeAddr = models.TextField()
	Department = models.TextField()
	Tel = models.CharField()
	MailAddr = models.CharField()
	Age = models.IntegerField()

class SecurityAccountInfo(models.Model):
	SecurityID = models.CharField()

class CapitalAccountInfo(models.Model):
	AccountID = models.CharField()
	Password = models.CharField()
	Isfirst = models.BooleanField(default=1)
	UserTable = models.ForeignKey(UserTable)
	BuyPassword = models.CharField()
	SecurityAccount = models.ForeignKey(SecurityAccountInfo)
	loginPwdWrongNum = models.IntegerField(default=0)
	transPwdWrongNum = models.IntegerField(default=0)
	lastTimeTrans = models.DateTimeField()
	lastTimeLogin = models.DateTimeField()
	IsTransFreeze = models.BooleanField()
	IsLoginFreeze = models.BooleanField()



