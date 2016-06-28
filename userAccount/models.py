#coding:utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib import admin

# Create your models here.
class UserTable(models.Model):
    # 证券账户基本信息
    # SecurityID = models.ForeignKey(SecurityAccountInfo)
    SecurityID = models.CharField(max_length=20)
    Name = models.CharField(max_length=20)
    IDcard = models.CharField(max_length=20)
    Phone = models.CharField(max_length=20)
    Gender = models.IntegerField()
    Address = models.CharField(max_length=20)
    Career = models.CharField(max_length=20)
    Education = models.CharField(max_length=20)
    Company = models.CharField(max_length=20)
    IsFreeze=models.IntegerField()#是否冻结

	# 资金账户基本信息
    # AccountID = models.ForeignKey(CapitalAccountInfo)
    AccountID = models.CharField(max_length=20)
    Username=models.CharField(max_length=20)
    Balance = models.FloatField(max_length=80)
    LoginPasswd=models.CharField(max_length=20)
    BuyPassword = models.CharField(max_length=20)#trans_passwd



    # date_joined = models.DateField()
 
    def __unicode__(self):
        data = self.SecurityID + " " + self.IDcard
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
   
    def compSecurityAccount(self,SecurityIDtmp,nametmp,IDcardtmp,phonetmp):
        # return False
        if self.compSecurityID(SecurityIDtmp) and self.compname(nametmp) and self.compIDcard(IDcardtmp) and self.compphone(phonetmp):
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
    StuffID=models.CharField(max_length=20)
    StuddName=models.CharField(max_length=20)
    Password = models.CharField(max_length=20)


    def compStuffID(self,StuffIDtmp):
        return (self.StuffID == StuffIDtmp)
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


class UserAdmin(admin.ModelAdmin):
    list_display = ('IDcard','SecurityID','AccountID','Name','Username','Phone','Gender','Address','Career','Education','Company','IsFreeze','BuyPassword','LoginPasswd','Balance')
    
admin.site.register(UserTable,UserAdmin)

class StaffAdmin(admin.ModelAdmin):
	list_display=('StuddName','StuffID','Password')

admin.site.register(StaffTable,StaffAdmin)









