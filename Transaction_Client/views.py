from django.shortcuts import render
from Transaction_Client import functions
from django.http import HttpResponse
import datetime

# Create your views here.

def login(request):
	context = {}
	return render(request,'TransactionClient_login.html',context)

def logout(request):
	del request.session['ID']
	context = {}
	return render(request,'TransactionClient_login.html',context)


def check(request):
	username = request.POST['username']
	password = request.POST['password']
	username = str(username)
	password = str(password)
	res = functions.login(username, password)
	response = HttpResponse()
	print res
	if(res[0] == 1):
		request.session['ID'] = username
		response.write('<html><script type="text/javascript">alert("First Login Success!");window.location="/TransactionClient/faq/"</script></html>')
		return response
	if(res[0] == -1):
		response.write('<html><script type="text/javascript">alert("Wrong Username or Password!");window.location="../"</script></html>')
		return response
	if(res[0] == -2):
		response.write('<html><script type="text/javascript">alert("Frozen Account!");window.location="../"</script></html>')
		return response
	if(res[0] == -4):
		response.write('<html><script type="text/javascript">alert("Input wrong password too many times! The account will be frozen.");window.location="../"</script></html>')
		return response
	if(res[0] == 0):
		request.session['ID'] = username
		response.write('<html><script type="text/javascript">alert("Login Success");window.location="/TransactionClient/capital"</script></html>')
		return response

def modipasswd(request):
	username = request.session.get('ID', default=None)
	passwd = request.POST["change_password"]
		
	orig_passwd = request.POST['orig_passwd']
	new_passwd = request.POST['new_passwd']
	confirm_passwd = request.POST['confirm_passwd']

	response = HttpResponse()
	if(confirm_passwd != new_passwd):
		response.write('<html><script type="text/javascript">alert("The new and confirmed passwords do not match. ");window.location="/TransactionClient/password/"</script></html>')
		return response

	if(passwd == "login"):
		res = functions.changeLoginPwd(username, orig_passwd, new_passwd)
		if(res == -1):
			response.write('<html><script type="text/javascript">alert("Wrong Original Password!");window.location="/TransactionClient/password/"</script></html>')
			return response
		if(res == -4):
			response.write('<html><script type="text/javascript">alert("Account will be frozen for inputting wrong passwords too many times!");window.location="/TransactionClient/password/"</script></html>')
			return response
		if(res == -2):
			del request.session['ID']
			response.write('<html><script type="text/javascript">alert("Accout Frozen!");window.location="/TransactionClient/"</script></html>')
			return response
		if(res == 0):
			response.write('<html><script type="text/javascript">alert("Modification Success!");window.location="/TransactionClient/password/"</script></html>')
			return response

	if(passwd == "payment"):
		res = functions.changeTransPwd(username, orig_passwd, new_passwd)
		if(res == -1):
			response.write('<html><script type="text/javascript">alert("Wrong Original Password!");window.location="/TransactionClient/password/"</script></html>')
			return response
		if(res == -4):
			response.write('<html><script type="text/javascript">alert("Account will be frozen for inputting wrong passwords too many times!");window.location="/TransactionClient/password/"</script></html>')
			return response
		if(res == -2):
			del request.session['ID']
			response.write('<html><script type="text/javascript">alert("Accout Frozen!");window.location="/TransactionClient/"</script></html>')
			return response
		if(res == 0):
			response.write('<html><script type="text/javascript">alert("Modification Success!");window.location="/TransactionClient/password/"</script></html>')
			return response


def password(request):
	username = request.session.get('ID', default=None)
	res = functions.checkLogin(username)
	if(res == 0):
		status = "Normal"
	if(res == -1):
		status = "Overtime"
	if(res == -2):
		status = "Frozen"
	return render(request, 'TransactionClient_password.html', {'username': username, 'status': status})

def capital(request):
	username = request.session.get('ID', default=None)
	resf = functions.checkLogin(username)
	if(resf == 0):
		status = "Normal"
	if(resf == -1):
		status = "Overtime"
	if(resf == -2):
		status = "Frozen"
	response = HttpResponse()
	res = functions.checkCapitalInfo(username)
	if(res[0] == -1):
		stock_value = "Error"
		balance = "Error"
	if(res[0] != -1):
		stock_value = res[0]
		balance = res[1]
	return render(request, 'TransactionClient_capital.html',{'stock_value':stock_value, 'balance': balance, 'username': username, 'status': status})

def possessed(request):
	username = request.session.get('ID', default=None)
	resf = functions.checkLogin(username)
	if(resf == 0):
		status = "Normal"
	if(resf == -1):
		status = "Overtime"
	if(resf == -2):
		status = "Frozen"
	PossessedList = functions.checkPossessedStock(username)
	return render(request, 'TransactionClient_possessed.html',{'PossessedList': PossessedList, 'username': username, 'status': status})

def stock(request):
	username = request.session.get('ID', default=None)
	resf = functions.checkLogin(username)
	if(resf == 0):
		status = "Normal"
	if(resf == -1):
		status = "Overtime"
	if(resf == -2):
		status = "Frozen"
	return render(request, 'TransactionClient_stock.html',{'username': username, 'status': status})

def transaction(request):
	username = request.session.get('ID', default=None)
	resf = functions.checkLogin(username)
	if(resf == 0):
		status = "Normal"
	if(resf == -1):
		status = "Overtime"
	if(resf == -2):
		status = "Frozen"
	if not request.POST.has_key("search"):
		return render(request, 'TransactionClient_transaction.html', {'username': username, 'status': status})
	search_method = request.POST["search"]
	if(search_method == "date"):
		startYear = request.POST["begin_year"]
		startMonth = request.POST["begin_month"]
		startDay = request.POST["begin_day"]

		endYear = request.POST["end_year"]
		endMonth = request.POST["end_month"]
		endDay = request.POST["end_day"]
		if(startYear==u'' or startMonth==u'' or startDay==u'' or endDay==u'' or endYear==u'' or endMonth==u''):
			return render(request, 'TransactionClient_transaction.html', {'username': username, 'status': status})
		startDate = datetime.date(int(startYear), int(startMonth), int(startDay))
		endDate = datetime.date(int(endYear), int(endMonth), int(endDay))
		TransactionList = functions.getRecordByDate(startDate, endDate, username)
		return render(request, 'TransactionClient_transaction.html', {'username': username, 'status': status, 'TransactionList': TransactionList})
	if(search_method == "stock"):
		StockID = request.POST["ticker"]
		TransactionList = functions.getRecordByStock(StockID, username)
		response = HttpResponse({'TransactionList': TransactionList})
		print StockID
		print TransactionList
		return render(request, 'TransactionClient_transaction.html', {'username': username, 'status': status, 'TransactionList': TransactionList})
	reaponse = HttpResponse()
	response.write('<html><script type="text/javascript">;window.location="/TransactionClient/transaction/"</script></html>')
	return response


def search(request):
	username = request.session.get('ID', default=None)
	search_method = request.POST["search"]
	if(search_method == "date"):
		startYear = request.POST["begin_year"]
		startMonth = request.POST["begin_month"]
		startDay = request.POST["begin_day"]
		startDate = datetime.date(int(startYear), int(startMonth), int(startDay))

		endYear = request.POST["end_year"]
		endMonth = request.POST["end_month"]
		endDay = request.POST["end_day"]
		endDate = datetime.date(int(endYear), int(endMonth), int(endDay))
		TransactionList = functions.getRecordByDate(startDate, endDate, username)
		response = HttpResponse({'TransactionList': TransactionList})
		response.write('<html><script type="text/javascript">;window.location="/TransactionClient/transaction/"</script></html>')
		return response
	if(search_method == "stock"):
		StockID = request.POST["ticker"]
		TransactionList = functions.getRecordByStock(StockID, username)
		response = HttpResponse({'TransactionList': TransactionList})
		print StockID
		print TransactionList
		response.write('<html><script type="text/javascript">;window.location="/TransactionClient/transaction/"</script></html>')
		return response
	reaponse = HttpResponse()
	response.write('<html><script type="text/javascript">;window.location="/TransactionClient/transaction/"</script></html>')
	return response

def purchase(request):
	username = request.session.get('ID', default=None)
	resf = functions.checkLogin(username)
	if(resf == 0):
		status = "Normal"
	if(resf == -1):
		status = "Overtime"
	if(resf == -2):
		status = "Frozen"
	return render(request, 'TransactionClient_purchase.html',{'username': username, 'status': status})

def sell(request):
	username = request.session.get('ID', default=None)
	resf = functions.checkLogin(username)
	if(resf == 0):
		status = "Normal"
	if(resf == -1):
		status = "Overtime"
	if(resf == -2):
		status = "Frozen"
	return render(request, 'TransactionClient_sell.html',{'username': username, 'status': status})

def faq(request):
	username = request.session.get('ID', default=None)
	resf = functions.checkLogin(username)
	if(resf == 0):
		status = "Normal"
	if(resf == -1):
		status = "Overtime"
	if(resf == -2):
		status = "Frozen"
	return render(request, 'TransactionClient_faq.html',{'username': username, 'status': status})

def unlogin(request):
	return render(request, 'TransactionClient_unlogin.html',{})

def purchase_stock_id_check(request):
	stockID = request.GET["stock_id"]
	res = functions.getStock(stockID)
	# print res[0]
	if(res[0] == -1):
		return HttpResponse("0");
	else:
		request.session['stockID'] = stockID
		stockInfo = res[1]
		return HttpResponse(str(stockInfo.StockName)+"#"+str(stockInfo.CurrentPrice)+"#"+str(stockInfo.MaxPrice)+"#"+str(stockInfo.MinPrice))
	
def purchase_stock(request):
	stockID = request.session.get('stockID', default=None)
	del request.session['stockID']
	# print stockID
	PurchasePrice = float(request.POST['PurchasePrice'])
	PurchaseAmount = int(request.POST['PurchaseAmount'])
	TransPwd = request.POST['trans_passwd']
	username = request.session.get('ID', default=None)
	buyingInfo = {'userID':username, 'stockID': stockID, 'Price':PurchasePrice, 'num':PurchaseAmount, 'TransPwd': TransPwd}
	print buyingInfo
	res = functions.checkBuying(buyingInfo)
	print res
	response = HttpResponse()
	if(res == 0):
		response.write('<html><script type="text/javascript">alert("Submit Success!");window.location="/TransactionClient/purchase/"</script></html>')
		return response
	if(res == -1):
		response.write('<html><script type="text/javascript">alert("Lack of balance!");window.location="/TransactionClient/purchase/"</script></html>')
		return response
	if(res == -2):
		response.write('<html><script type="text/javascript">alert("Price not in the range!");window.location="/TransactionClient/purchase/"</script></html>')
		return response
	if(res == -4):
		response.write('<html><script type="text/javascript">alert("System Error!");window.location="/TransactionClient/purchase/"</script></html>')
		return response
	if(res == -8):
		response.write('<html><script type="text/javascript">alert("Wrong Transaction Password!");window.location="/TransactionClient/purchase/"</script></html>')
		return response
	if(res == -32):
		response.write('<html><script type="text/javascript">alert("Account will be frozen for inputting wrong passwords too many times!");window.location="/TransactionClient/purchase/"</script></html>')
		return response
	if(res == -16):
		del request.session['ID']
		response.write('<html><script type="text/javascript">alert("Accout Frozen!");window.location="/TransactionClient/"</script></html>')
		return response


def sell_stock_id_check(request):
	stockID = request.GET["stock_id"]
	username = request.session.get('ID', default=None)
	res = functions.getPossessedStock(username, stockID)
	if(res[0] == -1):
		return HttpResponse("0");
	else:
		request.session['stockID'] = stockID
		stockInfo = res[1]
		print stockInfo.CurrentPrice
		return HttpResponse(str(stockInfo.StockName)+"#"+str(stockInfo.CurrentPrice)+"#"+str(stockInfo.MaxPrice)+"#"+str(stockInfo.MinPrice))

def sell_stock(request):
	stockID = request.session.get('stockID', default=None)
	del request.session['stockID']
	# print stockID
	sellPrice = float(request.POST['sellPrice'])
	sellAmount = int(request.POST['sellAmount'])
	TransPwd = request.POST['trans_passwd']
	username = request.session.get('ID', default=None)
	SalingInfo = {'userID':username, 'stockID': stockID, 'Price':sellPrice, 'num':sellAmount, 'TransPwd': TransPwd}
	res = functions.checkSaling(SalingInfo)
	response = HttpResponse()
	if(res == 0):
		response.write('<html><script type="text/javascript">alert("Submit!");window.location="/TransactionClient/sell/"</script></html>')
		return response
	if(res == -1):
		response.write('<html><script type="text/javascript">alert("Lack of stock!");window.location="/TransactionClient/sell/"</script></html>')
		return response
	if(res == -2):
		response.write('<html><script type="text/javascript">alert("Price not in the range!");window.location="/TransactionClient/sell/"</script></html>')
		return response
	if(res == -4):
		response.write('<html><script type="text/javascript">alert("System Error!");window.location="/TransactionClient/sell/"</script></html>')
		return response
	if(res == -8):
		response.write('<html><script type="text/javascript">alert("Wrong Transaction Password!");window.location="/TransactionClient/purchase/"</script></html>')
		return response
	if(res == -32):
		response.write('<html><script type="text/javascript">alert("Account will be frozen for inputting wrong passwords too many times!");window.location="/TransactionClient/purchase/"</script></html>')
		return response
	if(res == -16):
		del request.session['ID']
		response.write('<html><script type="text/javascript">alert("Accout Frozen!");window.location="/TransactionClient/"</script></html>')
		return response