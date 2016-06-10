
#!/usr/bin/env python
import os
import sys

from django.apps import apps
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Stock_Trading_System.settings")
from django.core.management import execute_from_command_line
execute_from_command_line(sys.argv)


from Transaction_Client.functions import *

def testLogin():
	res = login('c34', '123456')
	print(res)

	res = login('c34', '11111')
	print(res)
	res = login('c34', '11111')
	print(res)
	res = login('c34', '11111')
	print(res)

	res = login('c34', '11111')
	print(res)

def testCheckLogin():
	res = checkLogin('c34')
	print(res)

def testChangeLoginPwd():
	res = changeLoginPwd('c34', '123456', '654321')
	print(res)

	res = changeLoginPwd('c34', '123456', '123456')
	print(res)


if __name__ == "__main__":
	testLogin()
	testCheckLogin()
	testChangeLoginPwd()
