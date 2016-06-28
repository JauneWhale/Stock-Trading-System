import os
import sys
import datetime

from django.db import models
from django.utils import timezone

from database.models import *

maxPwdWrongNum = 3

def check_login(userName, password):
    res = CapitalAccountInfo.objects.filter(AccountID=userName)
    if (res):
        account = res[0]
        if (account.lastTimeLogin + datetime.timedelta(days=1) < timezone.now()):
            account.IsLoginFreeze = False
            account.loginPwdWrongNum = 0
        if (account.IsLoginFreeze):
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
    else: return (-1, None)

def check_trans(userName, password):
    res = CapitalAccountInfo.objects.filter(AccountID=userName)
    if res:
        account = res[0]
        if (account.lastTimeTrans + datetime.timedelta(days=1) < timezone.now()):
            account.IsTransFreeze = False
            account.transPwdWrongNum = 0
        if (account.IsTransFreeze):
            return (-2, None)
        account.lastTimeTrans = timezone.now() 
        account.save()
        if (account.BuyPassword == password):
            return (0, account)
        else:
            WN = account.transPwdWrongNum + 1
            account.transPwdWrongNum += 1
            if (WN >= maxPwdWrongNum):
                account.IsTransFreeze = True
                account.save()
                return (-4, None)
            else:
                account.save()
                return (-1, None)
    else:
        return (-1, None)

def login(userName, password):
    res = check_login(userName, password)
    if (res[0] != 0):
        return res

    if (res[1].Isfirst):
        res[1].Isfirst = False
        res[1].save()
        return (1, res[1])
    else:
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
    res = check_login(userID, oldPwd)
    if (res[0] == 0):
        account = res[1] 
        account.Password = newPwd
        account.save()
    return res[0]

def changeTransPwd(userID, oldPwd, newPwd):
    res = check_trans(userID, oldPwd)
    if (res[0] == 0):
        account = res[1]
        account.BuyPassword = newPwd
        account.save()
    return res[0]

def getStock(stockID):
    res = StockInfo.objects.filter(StockID=stockID)
    if res:
        return (0, res[0])
    else:
        return (-1, None)

def checkBuying(buyingInfo):
    res = check_trans(buyingInfo['userID'], buyingInfo['TransPwd'])
    if (res[0] < 0):
        return res[0] * 16
    res = StockInfo.objects.filter(StockID=buyingInfo['stockID'])

    if res:
        stock = res[0]
        print buyingInfo['Price']
        print stock.CurrentPrice
        print stock.MaxPrice
        print stock.MinPrice
        capital = CapitalInfo.objects.filter(AccountID=buyingInfo['userID'])
        if capital:
            if (buyingInfo['Price'] * buyingInfo['num'] > capital[0].ActiveMoney):
                return -1
        else:
            return -4
        if (buyingInfo['Price'] > stock.CurrentPrice * (1 + stock.UpLimit)):
            return -2
        if (buyingInfo['Price'] < stock.CurrentPrice * (1 - stock.BottomLimit)):
            return -2
        if (stock.State):
            return -8
        return 0
    else:
            return -4

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

def getSecurityAccountID(userID):
    c_res = CapitalAccountInfo.objects.filter(AccountID=userID)
    if c_res:
        accountID = c_res[0].SecurityAccount.SecurityID
        return accountID
    else:
        return -1

def checkSaling(salingInfo):
    res = check_trans(salingInfo['userID'], salingInfo['TransPwd'])
    if (res[0] < 0):
        return res[0] * 16
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
                return -2
            if (salingInfo['Price'] < stock.CurrentPrice * (1 - stock.BottomLimit)):
                return -2
            if (stock.State):
                return -8
            return 0
        else:
            return -4
    else:
        return -4

def checkCapitalInfo(userID):
	res = CapitalInfo.objects.filter(AccountID=userID)
	stocks = checkPossessedStock(userID)
	stock_value = 0;
	if stocks:
		for s in stocks:
			stock_value += s[3] * s[4]
			
	if res:
		return (stock_value, res[0])
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

def getRecordByDate(startDate, endDate, userID):
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

def getRecordByStock(stockID, userID):
    dealed = InstDealed.objects.filter(AccountID__AccountID=userID, StockID=stockID)
    undealed = InstNotDealed.objects.filter(AccountID__AccountID=userID, StockID=stockID)
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
