#coding:utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib import admin

# Create your models here.
class UserTable(models.Model):
    # 证券账户基本信息
    # SecurityID = models.ForeignKey(SecurityAccountInfo)
    # SecurityID = models.CharField(max_length=20)
    # UserID = models.CharField(max_length=20,primary_key=True)
    Name = models.CharField(max_length=20)
    IDcard = models.CharField(max_length=20,primary_key=True)
    Tel = models.CharField(max_length=20,default="")
    Gender = models.IntegerField()
    HomeAddr = models.TextField(default="")
    Occupation = models.CharField(max_length=20)
    EduInfo = models.CharField(max_length=20)
    Department = models.TextField(null=True)
    MailAddr = models.CharField(max_length=30,default="")
    Age = models.IntegerField(null=True)


    # date_joined = models.DateField()
 
    def __unicode__(self):
        data = self.IDcard + " " + self.Name
        return data

    def compSecurityID(self,SecurityIDtmp):
        return (self.SecurityID == SecurityIDtmp)
    
    def compname(self,nametmp):
        return (self.Name == nametmp)

    def compIDcard(self,IDcardtmp):
        return (self.IDcard == IDcardtmp)
    
    def compphone(self,phonetmp):
        return (self.Phone == phonetmp)

    def compAccountID(self,AccountIDtmp):
        return (self.AccountID == AccountIDtmp)

    def compPasswdInfo(self,SecurityIDtmp,IDcardtmp,AccountIDtmp):
    	if self.compSecurityID(SecurityIDtmp) and self.compIDcard(IDcardtmp) and self.compAccountID:
    		return True
    	else:
    		return False
   
    def compPasswdInfo(self,SecurityIDtmp,IDcardtmp,AccountIDtmp):
        if self.compSecurityID(SecurityIDtmp) and self.compIDcard(IDcardtmp) and self.compAccountID:
            return True
        else:
            return False

    # def compBalance(self,SecurityIDtmp,AccountIDtmp):
    #     if (self.AccountID == AccountIDtmp and self.SecurityID == SecurityIDtmp):
    #         renturn Balance
    #     else :
    #         return False




class StaffTable(models.Model):
	#员工表
    StuffID=models.CharField(max_length=20,primary_key=True)
    StuddName=models.CharField(max_length=20)
    Password = models.CharField(max_length=20)


    def compStuffID(self,StuffIDtmp):
        return (self.StuffID == StuffIDtmp)
# 证券账户基本信息
class SecurityAccountInfo(models.Model):
    SecurityID = models.CharField(max_length=20,primary_key=True)
    IsFreeze=models.IntegerField(default=0)
    IDcard=models.ForeignKey(UserTable)

# 资金账户基本信息
class CapitalAccountInfo(models.Model):
    AccountID = models.CharField(max_length=20,primary_key=True) 
    # Password = models.CharField(max_length=20)
    Password=models.CharField(max_length=20)
    Isfirst = models.BooleanField(default=1)
    UserTable = models.ForeignKey(UserTable)
    BuyPassword = models.CharField(max_length=20)
    SecurityAccount = models.ForeignKey(SecurityAccountInfo)
    loginPwdWrongNum = models.IntegerField(default=0)
    transPwdWrongNum = models.IntegerField(default=0)
    lastTimeTrans = models.DateTimeField(null=True)
    lastTimeLogin = models.DateTimeField(null=True)
    IsTransFreeze = models.BooleanField(default=False)
    IsLoginFreeze = models.BooleanField(default=False)

# 资金信息
class CapitalInfo(models.Model):
    AccountID = models.ForeignKey(CapitalAccountInfo)
    ActiveMoney = models.FloatField(default="")
    # Balance = models.FloatField(max_length=80)
    FrozenMoney = models.FloatField()
    BankCard = models.CharField(max_length=20,null=True)


class UserAdmin(admin.ModelAdmin):
    list_display = ('Name','IDcard','Tel','Gender','HomeAddr','Occupation','EduInfo','Department','MailAddr','Age')
    
admin.site.register(UserTable,UserAdmin)

class StaffAdmin(admin.ModelAdmin):
	list_display=('StuddName','StuffID','Password')

admin.site.register(StaffTable,StaffAdmin)

# class SecurityAdmin(admin.ModelAdmin):
#     list_display=('SecurityID','IsFreeze')

class SecurityAdmin(admin.ModelAdmin):
    list_display=('SecurityID','IsFreeze','IDcard')

admin.site.register(SecurityAccountInfo,SecurityAdmin)









