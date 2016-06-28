# coding:utf-8
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from database.models import StockManage
from database.models import StockInfo
import central

# Create your views here.

def home(request):
    try:
        ID = request.GET['id']
    except:
        ID = "001"
    return render(request, 'trade_manage.html', {"sid": ID})


#返回股票的列表
def GetStockInfo(request):
    adminID = request.GET['id']
    StocksInfoList = []
     # StockID, StockName, Amount, CurrentPrice, QuoteChange, UpLimit, DownLimit, State
    stocks = StockManage.objects.filter(AdminID=adminID)#缺
    if len(stocks) == 0:
        stocks = StockInfo.objects.all()
    for Stock in stocks:
        if len(stocks) == 0:
            stock = Stock
        else:
            stock = Stock.StockID
        temp = {}
        temp['id'] = stock.StockID
        temp['name'] = stock.StockName
        temp['price'] = stock.CurrentPrice
        temp['volume'] = stock.Quantity
        temp['change'] = (stock.CurrentPrice - stock.TodayOpeningPrice) / stock.TodayOpeningPrice
        temp['state'] = stock.State
        temp['price_limit'] = stock.UpLimit
        StocksInfoList.append(temp)
    # 临时显示用数据
    '''
    stock1 = {}
    stock1['id'] = 'SS10001'
    stock1['name'] = 'China Telecom'
    stock1['price'] = 103.21
    stock1['volume'] = 12031
    stock1['change'] = '+1.30'
    stock1['state'] = 1
    stock1['price_limit'] = 10
    stock2 ={}
    stock2['id'] = 'SS10002'
    stock2['name'] = 'China Mobile'
    stock2['volume'] = 22358
    stock2['price'] = 257.75
    stock2['change'] = '-0.32'
    stock2['state'] = 1
    stock2['price_limit'] = 8
    stock3 ={}
    stock3['id'] = 'SS10003'
    stock3['name'] = 'China Unicom'
    stock3['volume'] = 2395
    stock3['price'] = 52.98
    stock3['change'] = '0.00'
    stock3['state'] = 0
    stock3['price_limit'] = 8
    StocksInfoList = [stock1, stock2, stock3]
    '''
    return JsonResponse(StocksInfoList, safe=False)

#返回列表
def GetStockList(request):
    stockID = request.GET['id']
    StockList = central.interface.admin_query(stockID)
    '''
    StockList = {}
    # Price, Buy
    # 临时显示用数据
    buy_list = []
    buy_list.append({"id": "B001", "p_id": "00029", "price": 102.20, "amount": 100})
    sell_list = []
    sell_list.append({"id": "S021", "s_id": "00106", "price": 103.20, "amount": 150})
    StockList = {"buy_list": buy_list, "sell_list": sell_list}
    '''
    return JsonResponse(StockList, safe=False)

#以下三个成功返回1，失败返回0
def FreezeStock(request):
    stockID = request.GET['id']
    try:
        central.interface.froze(stockID)
        data = {'state': 1}
    except:
        data = {'state': 0}
    return JsonResponse(data, safe=False)

def RemuseStock(request):
    stockID = request.GET['id']
    try:
        central.interface.renew(stockID)
        data = {'state': 1}
    except:
        data = {'state': 0}
    return JsonResponse(data, safe=False)

def SetLimit(request):
    stockID = request.GET['id']
    up = request.GET['up']
    limit = request.GET['limit']
    try:
        stock = StockInfo.objects.get(StockID=stockID)
        if int(up) == 1:
            stock.UpLimit = float(limit)
        else:
            stock.BottomLimit = float(limit)
        stock.save()
        data = {'state': 1}
    except:
        data = {'state': 0}
    return JsonResponse(data, safe=False)