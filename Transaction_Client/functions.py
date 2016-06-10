import os
import sys
import datetime

from django.db import models
from django.utils import timezone

from database.models import *

maxPwdWrongNum = 3

def check(userName, password):
    res = CapitalAccountInfo.objects.filter(AccountID=userName)
    if (res):
        account = res[0]
        if (account.IsLoginFreeze):
            if (account.lastTimeLogin + datetime.timedelta(days=1) < timezone.now()):
                account.IsLoginFreeze = False
            else:
                return (-2, None)
        account.lastTimeLogin = timezone.now()
        account.save()
        if (account.Password == password):
            return (0, account)
        else:
            WN = account.loginPwdWrongNum + 1
            account.loginPwdWrongNum += 1
            if (WN >= maxPwdWrongNum):
                account.IsLoginFreeze = True
                account.save()
                return (-4, None)
            else:
                account.save()
                return (-1, None)
    else:
        return (-1, None)

def login(userName, password):
    res = check(userName, password)
    if (res[0] == 0):
        account = res[1]
        account.lastTimeLogin = timezone.now()
        account.save()
    return res

def checkLogin(userID):
    res = CapitalAccountInfo.objects.filter(AccountID=userID)
    if res:
        account = res[0]
        if (account.IsLoginFreeze):
            return -2
        if (account.lastTimeLogin + datetime.timedelta(hours=5) < timezone.now()):
            return -1
        return 0
    else:
        return -1


def changeLoginPwd(userID, oldPwd, newPwd):
    res = check(userID, oldPwd)
    if (res[0] == 0):
        account = res[1] 
        account.Password = newPwd
        account.save()
    return res[0]

def changeTransPwd(userID, oldPwd, newPwd):
    res = CapitalAccountInfo.objects.filter(AccountID=userID)
    if res:
        account = res[0]
        if (account.IsTransFreeze):
            return -2
        if (account.BuyPassword == oldPwd):
            account.BuyPassword = newPwd
            account.save()
            return 0
        else:
            account.transPwdWrongNum += 1
            if (account.transPwdWrongNum >= maxPwdWrongNum):
                account.IsTransFreeze = True
                account.save()
                return -4
            else:
                account.save()
                return -1
    else:
        return -1

def getStock(stockID):
    res = StockInfo.objects.filter(StockID=stockID)
    if res:
        return (0, res[0])
    else:
        return (-1, None)

def checkBuying(buyingInfo):
    res = StockInfo.objects.filter(StockID=buyingInfo['stockID'])
    if res:
        stock = res[0]
        if (buyingInfo['Price'] > stock.CurrentPrice * (1 + stock.UpLimit)):
            return -1
        if (buyingInfo['Price'] < stock.CurrentPrice * (1 - stock.BottomLimit)):
            return -1
        return 0
    else:
        return -1

def getPossessedStock(userID, stockID):
    c_res = CapitalAccountInfo.objects.filter(AccountID=userID)
    if c_res:
        account = c_res[0].SecurityAccount
        s_res = SecurityStockInfo.objects.filter(SecurityID=account.SecurityID, StockID=stockID)
        if (s_res):
            stock = StockInfo.objects.get(StockID=stockID)
            return (0, stock)
        else:
            return (-1, None)
    else:
        return -1

def checkSaling(salingInfo):
    c_res = CapitalAccountInfo.objects.filter(AccountID=salingInfo['userID'])
    if c_res:
        account = c_res[0].SecurityAccount
        s_res = SecurityStockInfo.objects.filter(SecurityID=account.SecurityID, StockID=salingInfo['stockID'])
        if s_res:
            pstock = s_res[0]
            if (pstock.ShareHolding < salingInfo['num']):
                return -1
            stock = StockInfo.objects.get(StockID=pstock.StockID)
            if (salingInfo['Price'] > stock.CurrentPrice * (1 + stock.UpLimit)):
                return -1
            if (salingInfo['Price'] < stock.CurrentPrice * (1 - stock.BottomLimit)):
                return -1
            return 0
        else:
            return -1
    else:
        return -1

def checkCapitalInfo(userID):
    res = CapitalInfo.objects.filter(AccountID=userID)
    if res:
        return (0, res[0])
    else:
        return (-1, None)

def checkPossessedStock(userID):
    ret = CapitalAccountInfo.objects.filter(AccountID=userID)
    if ret:
        account = ret[0].SecurityAccount;
        stocks = SecurityStockInfo.objects.filter(SecurityID=account.SecurityID)
        res = []
        for stock in stocks:
           s = StockInfo.objects.get(StockID = stock.StockID)
           if s:
               res.append((s.StockID, s.StockName, stock.BuyPrice, stock.ShareHolding, s.CurrentPrice, stock.status))
        return res
    else:
        return None

def getRecord(startDate, endDate, userID):
    dealed = InstDealed.objects.filter(AccountID__AccountID=userID, TimeSubmit__lte=endDate,
            TimeSubmit__gte=startDate)
    undealed = InstNotDealed.objects.filter(AccountID__AccountID=userID, TimeSubmit__lte=endDate,
            TimeSubmit__gte=startDate)
    records = []
    for r in dealed:
        stock = StockInfo.objects.get(StockID=r.StockID)
        records.append((r.TimeSubmit, r.StockID, stock.StockName, r.InstType, r.Quantity, r.PriceSubmit, 
            r.Quantity * r.PriceSubmit, 0))
    for r in undealed:
        stock = StockInfo.objects.get(StockID=r.StockID)
        records.append((r.TimeSubmit, r.StockID, stock.StockName, r.InstType, r.Quantity, r.PriceSubmit, 
            r.Quantity * r.PriceSubmit, 1))
    records.sort(key = lambda r : r[0])
    return records
