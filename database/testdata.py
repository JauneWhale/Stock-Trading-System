from database.models import *

from django.utils import timezone

userTable = UserTable(UserID='123',Name='123',IDcard='123');

securityAccount = SecurityAccountInfo(SecurityID='123');

capitalAccount = CapitalAccountInfo(AccountID='123',UserTable=userTable,SecurityAccount=securityAccount);

capitalInfo = CapitalInfo(AccountID='123')

stockInfo = StockInof(StockName='aaa',StockID='111');

userTable.save()
securityAccount.save()
capitalAccount.save()
capitalInfo.save()