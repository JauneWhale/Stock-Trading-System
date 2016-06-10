import datetime
import random

from django.test import TestCase
from django.utils import timezone

from database.models import *
from .functions import *
# Create your tests here.

stock = []
capital = CapitalInfo(AccountID='c34', ActiveMoney='65536',
		FrozenMoney='4096', BankCard='123456789')

def create_account():
	securityAccount = SecurityAccountInfo(SecurityID='1024')
	securityAccount.save()
	user = UserTable(UserID='c34', Name='vincent', IDcard='000000', 
			Gender=1, Occupation='student', EduInfo='college',
			HomeAddr='1107', Department='CS', Tel='18868100350', 
			MailAddr='c-34@qq.com', Age=21)
	user.save()
	account = CapitalAccountInfo(AccountID='c34', Password='123456', 
			Isfirst = False, BuyPassword='111111', 
			loginPwdWrongNum=0, transPwdWrongNum=0,
			UserTable = user, SecurityAccount = securityAccount, 
			lastTimeTrans=timezone.now(), lastTimeLogin=timezone.now(), 
			IsLoginFreeze=False, IsTransFreeze=False)
	account.save()
	capital.save()

def create_stock():
	stock.append(StockInfo(StockName='Zju', StockID='110110', CurrentPrice=10.24,
			MaxPrice=11.0, MinPrice=9.7, TodayOpeningPrice=9.9,
			YesterdayClosingPrice=9.7, Quantity=123321, UpLimit=0.07, BottomLimit=0.08))
	stock[0].save()
	stock.append(StockInfo(StockName='Django', StockID='119120', CurrentPrice=100.24,
			MaxPrice=108, MinPrice=98, TodayOpeningPrice=99,
			YesterdayClosingPrice=98.8, Quantity=654456, UpLimit=0.07, BottomLimit=0.08))
	stock[1].save()

def allocate_stock():
	SecurityStockInfo.objects.create(SecurityID='1024', StockID='110110',
			ShareHolding=2333, status=1, BuyPrice=9.2)
	SecurityStockInfo.objects.create(SecurityID='1024', StockID='119120',
			ShareHolding=322, status=0, BuyPrice=111)

def create_record():
	account = CapitalAccountInfo.objects.get(AccountID='c34')
	securityAccount = SecurityAccountInfo(SecurityID='1024')
	account.save()
	securityAccount.save()
	for i in range(10):
		InstDealed.objects.create(InstID='20160609%d' % i, 
				TimeSubmit=timezone.now() - datetime.timedelta(hours=random.randint(0,10)),
				TimeDealed=timezone.now(), InstType=random.randint(0,1), StockID='110110',
				AccountID=account, SecurityID=securityAccount, Quantity=100, PriceSubmit=10.0,
				PriceDealed=11.0)
	for i in range(10):
		InstNotDealed.objects.create(InstID='20160609%d' % (i + 10),
				TimeSubmit=timezone.now() - datetime.timedelta(hours=random.randint(0,10)),
				TimeOutOfDate=timezone.now(), InstType=random.randint(0,1), StockID='110110',
				AccountID=account, SecurityID=securityAccount, Quantity=100, PriceSubmit=10.0,
				InstState=0)

class LoginTests(TestCase):
	#test 0
	def test_login(self):
		create_account()

		res = login('c34', '123456')
		self.assertEqual(res[0], 0)
		res = login('c34', '111111')
		self.assertEqual(res[0], -1)
		res = login('c34', '111111')
		self.assertEqual(res[0], -1)

		res = login('c34', '111111')
		self.assertEqual(res[0], -4)
		
		res = login('c34', '123456')
		self.assertEqual(res[0], -2)
	
	#test 1
	def test_changeLoginPwd(self):
		create_account()

		res = changeLoginPwd('c34', '123456', '654321')
		self.assertEqual(res, 0)

		res = changeLoginPwd('c34', '123456', '123456')
		self.assertEqual(res, -1)

	#test 2
	def test_changeTransPwd(self):
		create_account()

		res = changeTransPwd('c34', '111111', '222222')
		self.assertEqual(res, 0)

		res = changeTransPwd('c34', '111111', '222222')
		self.assertEqual(res, -1)

	#test 3
	def test_getStock(self):
		create_stock()

		res = getStock('110110')
		self.assertEqual(res[0], 0)
		self.assertEqual(res[1].StockID, '110110')

	#test 4
	def test_checkBuying(self):
		create_account()
		create_stock()
		allocate_stock()

		buyingInfo = {'userID':'c34', 'stockID':'110110', 'Price':10.33, 'num':1000}
		res = checkBuying(buyingInfo)
		self.assertEqual(res, 0)
		
		buyingInfo = {'userID':'c34', 'stockID':'110110', 'Price':12.33, 'num':1000}
		res = checkBuying(buyingInfo)
		self.assertEqual(res, -1)

		buyingInfo = {'userID':'c34', 'stockID':'119120', 'Price':10.33, 'num':1000}
		res = checkBuying(buyingInfo)
		self.assertEqual(res, -1)

		buyingInfo = {'userID':'c34', 'stockID':'119120', 'Price':103.3, 'num':1000}
		res = checkBuying(buyingInfo)
		self.assertEqual(res, 0)
	
	#test 5
	def test_getPossessedStock(self):
		create_account()
		create_stock()
		allocate_stock()

		res = getPossessedStock('c34', '110110')
		self.assertEqual(res, (0, stock[0]))
		res = getPossessedStock('c34', '119120')
		self.assertEqual(res, (0, stock[1]))

		res = getPossessedStock('c34', '123123')
		self.assertEqual(res, (-1, None))

	#test 6
	def test_checkSaling(self):
		create_account()
		create_stock()
		allocate_stock()

		salingInfo = {'userID':'c34', 'stockID':'110110', 'Price':10.33, 'num':300}
		res = checkSaling(salingInfo)
		self.assertEqual(res, 0)

		salingInfo = {'userID':'c34', 'stockID':'110110', 'Price':10.33, 'num':3000}
		res = checkSaling(salingInfo)
		self.assertEqual(res, -1)
		
		salingInfo = {'userID':'c34', 'stockID':'110110', 'Price':11.90, 'num':300}
		res = checkSaling(salingInfo)
		self.assertEqual(res, -1)

		salingInfo = {'userID':'c34', 'stockID':'111111', 'Price':10.33, 'num':300}
		res = checkSaling(salingInfo)
		self.assertEqual(res, -1)

		salingInfo = {'userID':'cc', 'stockID':'111111', 'Price':10.33, 'num':300}
		res = checkSaling(salingInfo)
		self.assertEqual(res, -1)

		salingInfo = {'userID':'cc', 'stockID':'119120', 'Price':108.3, 'num':300}
		res = checkSaling(salingInfo)
		self.assertEqual(res, -1)

	#test 7
	def test_checkCapitalInfo(self):
		create_account()
		create_stock()
		create_stock()

		res = checkCapitalInfo('c34')
		self.assertEqual(res, (0, capital))

		res = checkCapitalInfo('vincent')
		self.assertEqual(res, (-1, None))

	#test 8
	def test_checkPossessedStock(self):
		create_account()
		create_stock()
		allocate_stock()

		res = checkPossessedStock('c34')
		self.assertEqual(res, 
				[('110110', 'Zju', 9.2, 2333, 10.24, 1),
					('119120', 'Django', 111.0, 322, 100.24, 0)])


		res = checkPossessedStock('vincent')
		self.assertEqual(res, None)

	#test 9
	def test_getRecord(self):
		create_account()
		create_stock()
		create_record()
		allocate_stock()
		
		res = getRecord(startDate=timezone.now() - datetime.timedelta(days=1), endDate=timezone.now(), userID='c34')
		self.assertNotEqual(res, None)
		print(res)

