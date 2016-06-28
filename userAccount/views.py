# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.template import RequestContext
from userAccount.models import UserTable
from django.http import HttpResponseRedirect
from userAccount.models import StaffTable
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

#定义表单模型
class UserForm(forms.Form):
	SecurityID = forms.CharField(label='SecurityID：',max_length=20)
	name = forms.CharField(label='用户名：',max_length=20)
	IDcard = forms.CharField(label='IDcard:',max_length=20)
	phone = forms.CharField(label='phone:',max_length=20)
	gender = forms.IntegerField(label='gender:')
	address = forms.CharField(max_length=20)
	occupation = forms.CharField(label='career:',max_length=20)
	education = forms.CharField(label='education:',max_length=20)
	company = forms.CharField(label='company:',max_length=20)
	#IsFree = forms.CharField(label='IsFreeze:',max_length=20)
	
class CapForm(forms.Form):
	SecurityID = forms.CharField(label='SecurityID：',max_length=20)
	CapitalID=forms.CharField(max_length=20)
	username=forms.CharField(max_length=20)
	IDcard = forms.CharField(label='IDcard:',max_length=20)
	#balance = forms.FloatField(label='余额：')
	login_passwd=forms.CharField(max_length=20)
	trans_passwd=forms.CharField(max_length=20)
	confirm_loginPasswd=forms.CharField(max_length=20)
	confirm_transPasswd=forms.CharField(max_length=20)
	name = forms.CharField(label='用户名：',max_length=20)
	phone = forms.CharField(label='phone:',max_length=20)
	gender = forms.IntegerField(label='gender:')
	address = forms.CharField(max_length=20)
	occupation = forms.CharField(label='career:',max_length=20)
	education = forms.CharField(label='education:',max_length=20)
	company = forms.CharField(label='company:',max_length=20)

class StuffForm(forms.Form):
	StuffID=forms.CharField(max_length=20)
	StuddName=forms.CharField(max_length=20)
	Password = forms.CharField(max_length=20)

@csrf_exempt
def login(request):
	context = {}
	tmp = ""

	staffid = ""
	staffname = ""
	password = ""
	

	context['result'] = 'initial'
	dictTmp = {}

	if request.POST:
		if request.POST.has_key(u'staffid'):
			staffid = request.POST[u'staffid'].encode('utf-8')
			# request.session['sessionid'] = staffid
		if request.POST.has_key(u'staffname'):
			staffname = request.POST[u'staffname'].encode('utf-8')
			request.session['sessionname'] = staffname
		if request.POST.has_key(u'password'):
			password = request.POST[u'password'].encode('utf-8')
		request.session['sessionstate'] = 'normal'
		request.session['sessionimage'] = 'headshot.png'

		if (staffname == "" or password == "" or staffid == ""):
			tmp = 1
			
		else:
			dictTmp['StuffID']=staffid
			dictTmp['StuddName']=staffname
			dictTmp['Password']=password
			sfData = StuffForm(dictTmp)

			if sfData.is_valid():
				sfDataTMP = StaffTable.objects.filter(StuffID=staffid)
				if(len(sfDataTMP)):
					sfTmp = sfDataTMP[0]
					if sfTmp.compStuffID(staffid):
						tmp = 2


		if  tmp == 1 :
			message = "登录失败！ "
			context['result'] = message
			return render(request,'userAccountLogin.html',context)
		if tmp == 2 :
			message = "登录成功！ "
			response = HttpResponseRedirect('/userAccount/homepage/')
			return response
		
		#context['result'] = message
	return render(request,'userAccountLogin.html',context)
		
@csrf_exempt
def homepage(request):
	context = {}

	context['name'] = request.session.get('sessionname',default=None)
	context['state'] = request.session.get('sessionstate',default=None)
	context['img'] = request.session.get('sessionimage',default=None)
	return render(request,'userHomepage.html',context)

	
@csrf_exempt
def openSA(request):
	context = {}

	context['name'] = request.session.get('sessionname',default=None)
	context['state'] = request.session.get('sessionstate',default=None)
	context['img'] = request.session.get('sessionimage',default=None)
	request.encoding='utf-8'

	# response = HttpResponse()
	# 标志位
	tmp = ""

	SecurityID = ""
	name = ""
	IDcard = ""
	phone = ""
	gender = ""
	address = ""
	career = ""
	education = ""
	company = ""
	message = ""
	IsFreeze="1"

	CapitalID=""

	context['result'] = 'initial'
	if request.POST:
		uf = UserForm(request.POST)
		print uf
		if uf.is_valid():
			if request.POST.has_key(u'SecurityID'):
				SecurityID = request.POST[u'SecurityID'].encode('utf-8')
			if request.POST.has_key(u'name'):
				name = request.POST[u'name'].encode('utf-8')
			if request.POST.has_key(u'IDcard'):
				IDcard = request.POST[u'IDcard'].encode('utf-8')
			if request.POST.has_key(u'phone'):
				phone = request.POST[u'phone'].encode('utf-8')
			if request.POST.has_key(u'gender'):
				gender = request.POST[u'gender'].encode('utf-8')
			if request.POST.has_key(u'address'):
				address = request.POST[u'address'].encode('utf-8')
			if request.POST.has_key(u'career'):
				career = request.POST[u'career'].encode('utf-8')
			if request.POST.has_key(u'education'):
				education = request.POST[u'education'].encode('utf-8')
			if request.POST.has_key(u'company'):
				company = request.POST[u'company'].encode('utf-8')

			print "test2"
			if (SecurityID == "" or name == "" or IDcard == "" or phone=="" or gender == "" or address == "" or career == "" or education == "" or company == ""):
				tmp = 1

			else:
				tmp = 2
				 #将表单写入数据库
				user = UserTable()
				security = SecurityAccountInfo()
				# capitalInfo = CapitalInfo()

				security.SecurityID = SecurityID
				user.Name = name
				user.IDcard = IDcard
				user.Tel = phone
				user.Gender = gender
				user.HomeAddr = address
				user.Occupation = career
				user.EduInfo = education
				user.Department = company
				security.IsFreeze=false
				#user.StuffID="null"
				#user.StuddName="null"
				#user.password="null"
				#user.AccountID="null"
				# capitalInfo.ActiveMoney=0
				#user.Passsword="null"
				#user.BuyPassword="null"

				user.save()
				security.save()


			if  tmp == 1 :
				message = "请将信息填写完整！ "
			if tmp == 2 :
				message = "开通成功！"

		context['result'] = message

		# if tmp == 3:
		# 	message = "开通失败！"
		# 最好是返回失败的原因

	else:
		uf=UserForm()

		

	return render(request, 'openSecurityAccount.html', context)

@csrf_exempt
def  openCA(request):
	context = {}
	context['name'] = request.session.get('sessionname',default=None)
	context['state'] = request.session.get('sessionstate',default=None)
	context['img'] = request.session.get('sessionimage',default=None)
	request.encoding='utf-8'

	# 标志位
	tmp = ""

	# 初始化
	SecurityID = ""
	CapitalID = ""
	IDcard = ""
	username = ""
	login_passwd = ""
	confirm_loginPasswd = ""
	trans_passwd = ""
	confirm_transPasswd = ""
	
	context['result'] = 'initial'
	if request.POST:
		if request.POST.has_key(u'SecurityID'):
			SecurityID = request.POST[u'SecurityID'].encode('utf-8')
		if request.POST.has_key(u'CapitalID'):
			CapitalID = request.POST[u'CapitalID'].encode('utf-8')
		if request.POST.has_key(u'IDcard'):
			IDcard = request.POST[u'IDcard'].encode('utf-8')
		if request.POST.has_key(u'username'):
			username = request.POST[u'username'].encode('utf-8')
		if request.POST.has_key(u'login_passwd'):
			login_passwd = request.POST[u'login_passwd'].encode('utf-8')
		if request.POST.has_key(
			u'confirm_loginPasswd'):
			confirm_loginPasswd = request.POST[u'confirm_loginPasswd'].encode('utf-8')
		if request.POST.has_key(u'trans_passwd'):
			trans_passwd = request.POST[u'trans_passwd'].encode('utf-8')
		if request.POST.has_key(u'confirm_transPasswd'):
			confirm_transPasswd = request.POST[u'confirm_transPasswd'].encode('utf-8')
	
		if (SecurityID == "" or CapitalID == "" or username == "" or IDcard == "" or login_passwd== "" or confirm_loginPasswd == "" or trans_passwd == "" or confirm_transPasswd == "" ):
			tmp = 1
		else:
			UserTable.objects.filter(SecurityID=SecurityID,IDcard=IDcard).update(AccountID=CapitalID,ActiveMoney=0,BuyPassword=trans_passwd,Password=login_passwd,Username=username)
			tmp = 2

		if  tmp == 1 :
			message = "请将信息填写完整!"
		if tmp == 2 :
			message = "开通成功!"
		# if tmp == 3:
		# 	message = "开通失败！"
		# 最好是返回失败的原因
	
		context['result'] = message

	return render(request, 'openCapitalAccount.html', context)

@csrf_exempt
def reportSecurityLoss(request):
	context = {}
	context['name'] = request.session.get('sessionname',default=None)
	context['state'] = request.session.get('sessionstate',default=None)
	context['img'] = request.session.get('sessionimage',default=None)
	request.encoding='utf-8'

	# 标志位
	tmp = ""

	phone = ""
	SecurityID = ""
	name = ""
	IDcard = ""
	IsFreeze=""

	context['result'] = 'initial'
	#用于存放生成信息的词典
	dictTmp = {}

	if request.POST:
		if request.POST.has_key(u'SecurityID'):
			SecurityID = request.POST[u'SecurityID'].encode('utf-8')
		if request.POST.has_key(u'IDcard'):
			IDcard = request.POST[u'IDcard'].encode('utf-8')
		if request.POST.has_key(u'name'):
			name = request.POST[u'name'].encode('utf-8')
		if request.POST.has_key(u'phone'):
			phone = request.POST[u'phone'].encode('utf-8')

		if phone == "" or SecurityID == "" or IDcard == "" or name=="":
			context['result'] = "请填写全部信息！"
			return render(request, 'reportSecurityLoss.html',context)
		else:
			dictTmp['SecurityID'] = SecurityID
			dictTmp['name'] = name
			dictTmp['IDcard'] = IDcard
			dictTmp['phone'] = phone
			#以下均为临时数据
			dictTmp['gender'] = "1"
			dictTmp['address'] = "initial"
			dictTmp['career'] = "initial"
			dictTmp['education'] = "initial"
			dictTmp['company'] = "initial"
			dictTmp['StuffID']="inital"
			dictTmp['StuddName']="inital"
			dictTmp['password']="inital"
			dictTmp['AccountID']="inital"
			dictTmp['Balance']=0
			dictTmp['Password']="inital"
			dictTmp['BuyPassword']="inital"
			dictTmp['AccountID']="inital"
			dictTmp['Username']="inital"
			dictTmp['IsFreeze']=1

			#创建临时数据
			userData = UserForm(dictTmp)

			if userData.is_valid():
				userDataTMP = UserTable.objects.filter(SecurityID=SecurityID,IDcard=IDcard,IsFreeze__exact =1)
				if(len(userDataTMP)):
					userTmp = userDataTMP[0]
					if userTmp.compSecurityAccount(SecurityID,name,IDcard,phone):
						UserTable.objects.filter(SecurityID=SecurityID,IDcard=IDcard).update(IsFreeze=0)
						print userDataTMP
		 	   	 		print "success!"
		 	   	 		context['result'] = "挂失成功！"
						return render(request, 'reportSecurityLoss.html',context)
		 	   	 	else:
		 	   	 		context['result'] = "请输入正确的姓名和电话！"
						return render(request, 'reportSecurityLoss.html',context)
				else:
					context['result'] = "并无对应的证券账户和资金账户！"
					return render(request, 'reportSecurityLoss.html',context)

	return render(request, 'reportSecurityLoss.html', context)

@csrf_exempt
def reportCapitalLoss(request):
	context = {}
	context['name'] = request.session.get('sessionname',default=None)
	context['state'] = request.session.get('sessionstate',default=None)
	context['img'] = request.session.get('sessionimage',default=None)
	request.encoding='utf-8'

	# 标志位
	tmp = ""

	# 初始化
	SecurityID = ""
	CapitalID = ""
	username = ""
	IDcard = ""

	context['result'] = 'initial'
	#用于存放生成信息的词典
	dictTmp = {}

	if request.POST:
		if request.POST.has_key(u'SecurityID'):
			SecurityID = request.POST[u'SecurityID'].encode('utf-8')
		if request.POST.has_key(u'IDcard'):
			IDcard = request.POST[u'IDcard'].encode('utf-8')
		if request.POST.has_key(u'username'):
			username = request.POST[u'username'].encode('utf-8')
		if request.POST.has_key(u'CapitalID'):
			CapitalID = request.POST[u'CapitalID'].encode('utf-8')

		if CapitalID == "" or SecurityID == "" or IDcard == "" or username=="":
			context['result'] = "请填写全部信息！"
			return render(request, 'reportSecurityLoss.html',context)
		else:
			
			dictTmp['SecurityID'] = SecurityID
			dictTmp['IDcard'] = IDcard
			dictTmp['username']=username
			dictTmp['CapitalID']=CapitalID
			dictTmp['login_passwd']="inital"
			dictTmp['trans_passwd']="inital"
			dictTmp['confirm_loginPasswd']="inital"
			dictTmp['confirm_transPasswd']="inital"
			dictTmp['IsFreeze']=0
			dictTmp['phone'] = "initial"
			dictTmp['name'] = "initial"
			dictTmp['gender'] = "1"
			dictTmp['address'] = "initial"
			dictTmp['career'] = "initial"
			dictTmp['education'] = "initial"
			dictTmp['company'] = "initial"



			#创建临时数据
			capData = CapForm(dictTmp)
			print capData
			if capData.is_valid():
				capDataTMP = UserTable.objects.filter(SecurityID=SecurityID,IDcard=IDcard,AccountID=CapitalID)
				if(len(capDataTMP)):
					userTmp = capDataTMP[0]
					if userTmp.compAccountID(CapitalID):
						UserTable.objects.filter(SecurityID=SecurityID,IDcard=IDcard,AccountID=CapitalID).update(IsFreeze=00)
						print capDataTMP
						print "success!"
		 	   	 		context['result'] = "挂失成功！"
						return render(request, 'reportSecurityLoss.html',context)
		 	   	 	else:
		 	   	 		context['result'] = "请输入正确的信息！"
						return render(request, 'reportSecurityLoss.html',context)
				else:
					context['result'] = "并无对应的证券账户和资金账户！"
					return render(request, 'reportSecurityLoss.html',context)

		# if tmp == 3:
		# 	message = "挂失失败"
		# 最好是返回失败的原因

		#context['result'] = message

	return render(request, 'reportCapitalLoss.html', context)

@csrf_exempt
def resubmitSA(request):
	context = {}
	context['name'] = request.session.get('sessionname',default=None)
	context['state'] = request.session.get('sessionstate',default=None)
	context['img'] = request.session.get('sessionimage',default=None)
	request.encoding='utf-8'
	
	# 标志位
	tmp = ""

	SecurityID = ""
	name = ""
	IDcard = ""
	phone = ""
	gender = ""
	address = ""
	career = ""
	education = ""
	company = ""
	IsFreeze="1"

	context['result'] = 'initial'
	#用于存放生成信息的词典
	dictTmp = {}

	if request.POST:
		if request.POST.has_key(u'SecurityID'):
			SecurityID = request.POST[u'SecurityID'].encode('utf-8')
		if request.POST.has_key(u'name'):
			name = request.POST[u'name'].encode('utf-8')
		if request.POST.has_key(u'IDcard'):
			IDcard = request.POST[u'IDcard'].encode('utf-8')
		if request.POST.has_key(u'phone'):
			phone = request.POST[u'phone'].encode('utf-8')
		if request.POST.has_key(u'gender'):
			gender = request.POST[u'gender'].encode('utf-8')
		if request.POST.has_key(u'address'):
			address = request.POST[u'address'].encode('utf-8')
		if request.POST.has_key(u'career'):
			career = request.POST[u'career'].encode('utf-8')
		if request.POST.has_key(u'education'):
			education = request.POST[u'education'].encode('utf-8')
		if request.POST.has_key(u'company'):
			company = request.POST[u'company'].encode('utf-8')

	
		if (SecurityID == "" or name == "" or IDcard == "" or phone=="" or gender == "" or address == "" or career == "" or education == "" or company == ""):
			tmp = 1
		else:
			
			dictTmp['SecurityID'] = SecurityID
			dictTmp['name'] = name
			dictTmp['IDcard'] = IDcard
			dictTmp['phone'] = phone
			#以下均为临时数据
			dictTmp['gender'] = "1"
			dictTmp['address'] = "initial"
			dictTmp['career'] = "initial"
			dictTmp['education'] = "initial"
			dictTmp['company'] = "initial"
			dictTmp['StuffID']="inital"
			dictTmp['StuddName']="inital"
			dictTmp['password']="inital"
			dictTmp['AccountID']="inital"
			dictTmp['Balance']=0
			dictTmp['Password']="inital"
			dictTmp['BuyPassword']="inital"
			dictTmp['AccountID']="inital"
			dictTmp['Username']="inital"
			dictTmp['IsFreeze']="inital"

			userData=UserForm(dictTmp)
			if userData.is_valid():
				userDataTMP = UserTable.objects.filter(IDcard=IDcard)
				if(len(userDataTMP)):
					userTmp = userDataTMP[0]
					userTmp.delete()
		 	   	 	print "old delete success!"			#将表单写入数据库
		 	   	 	tmp = 2

			user = UserTable()
			# Security = compSecurityAccountInfo()


			user.SecurityID = SecurityID
			user.Name = name
			user.IDcard = IDcard
			user.Tel = phone
			user.Gender = gender
			user.HomeAddr = address
			user.Occupation = career
			user.EduInfo = education
			user.Department = company
			user.IsFreeze = 1
			#user.StuffID="null"
			#user.StuddName="null"
			#user.password="null"
			#user.AccountID="null"
			user.ActiveMoney=0
			#user.Password="null"
			#user.BuyPassword="null"

			user.save()


		if  tmp == 1 :
			message = "请将信息填写完整！ "
		if tmp == 2 :
			message = "补办成功！"
		# if tmp == 3:
		# 	message = "开通失败！"
		# 最好是返回失败的原因

		context['result'] = message

	return render(request, 'resubmitSecurityAccount.html', context)

@csrf_exempt
def resubmitCA(request):
	context = {}
	context['name'] = request.session.get('sessionname',default=None)
	context['state'] = request.session.get('sessionstate',default=None)
	context['img'] = request.session.get('sessionimage',default=None)
	request.encoding='utf-8'

	# 标志位
	tmp = ""

	# 初始化
	SecurityID = ""
	CapitalID = ""
	IDcard = ""
	username = ""
	login_passwd = ""
	confirm_loginPasswd = ""
	trans_passwd = ""
	confirm_transPasswd = ""

	context['result'] = 'initial'
	if request.POST:
		if request.POST.has_key(u'SecurityID'):
			SecurityID = request.POST[u'SecurityID'].encode('utf-8')
		if request.POST.has_key(u'CapitalID'):
			CapitalID = request.POST[u'CapitalID'].encode('utf-8')
		if request.POST.has_key(u'IDcard'):
			IDcard = request.POST[u'IDcard'].encode('utf-8')
		if request.POST.has_key(u'username'):
			username = request.POST[u'username'].encode('utf-8')
		if request.POST.has_key(u'login_passwd'):
			login_passwd = request.POST[u'login_passwd'].encode('utf-8')
		if request.POST.has_key(u'confirm_loginPasswd'):
			confirm_loginPasswd = request.POST[u'confirm_loginPasswd'].encode('utf-8')
		if request.POST.has_key(u'trans_passwd'):
			trans_passwd = request.POST[u'trans_passwd'].encode('utf-8')
		if request.POST.has_key(u'confirm_transPasswd'):
			confirm_transPasswd = request.POST[u'confirm_transPasswd'].encode('utf-8')

	
		if (SecurityID == "" or CapitalID == "" or username == "" or IDcard == "" or login_passwd== "" or confirm_loginPasswd == "" or trans_passwd == "" or confirm_transPasswd == "" ):
			tmp = 1
		else:
			dictTmp['SecurityID'] = SecurityID
			dictTmp['IDcard'] = IDcard
			dictTmp['username']="inital"
			dictTmp['CapitalID']=CapitalID
			dictTmp['login_passwd']="inital"
			dictTmp['trans_passwd']="inital"
			dictTmp['confirm_loginPasswd']="inital"
			dictTmp['confirm_transPasswd']="inital"
			dictTmp['IsFreeze']=0
			dictTmp['phone'] = phone
			dictTmp['name'] = name
			dictTmp['gender'] = "1"
			dictTmp['address'] = "initial"
			dictTmp['career'] = "initial"
			dictTmp['education'] = "initial"
			dictTmp['company'] = "initial"
			#创建临时数据
			capData = CapForm(dictTmp)
			if capData.is_valid():
				capDataTMP = UserTable.objects.filter(IDcard=IDcard)
				if(len(capDataTMP)):
					userTmp = capDataTMP[0]
					userTmp.delete()
					print "old delete success!"			#将表单写入数据库
					tmp = 2

			user = UserTable()
			user.SecurityID = SecurityID
			user.Name = name
			user.IDcard = IDcard
			user.Tel = phone
			user.Gender = gender
			user.HomeAddr = address
			user.Occupation = career
			user.EduInfo = education
			user.Department = company
			user.IsFreeze = 1
			user.AccountID=CapitalID
			user.ActiveMoney=0
			user.Password=login_passwd
			user.BuyPassword=trans_passwd

			user.save()


		if  tmp == 1 :
			message = "请将信息填写完整!"
		if tmp == 2 :
			message = "补办成功!"
		# if tmp == 3:
		# 	message = "补办失败！"
		# 最好是返回失败的原因
		context['result'] = message

	return render(request, 'resubmitCapitalAccount.html', context)

@csrf_exempt
def closeSA(request):
	context = {}
	context['name'] = request.session.get('sessionname',default=None)
	context['state'] = request.session.get('sessionstate',default=None)
	context['img'] = request.session.get('sessionimage',default=None)
	request.encoding='utf-8'

	# 标志位
	tmp = ""

	phone = ""
	SecurityID = ""
	name = ""
	IDcard = ""
	# response = HttpResponse()
	#print request.POST

	context['result'] = 'initial'
	#用于存放生成信息的词典
	dictTmp = {}

	#获取post的信息
	if request.POST:
		if request.POST.has_key(u'SecurityID'):
			SecurityID = request.POST[u'SecurityID'].encode('utf-8')
		if request.POST.has_key(u'name'):
			name = request.POST[u'name'].encode('utf-8')
		if request.POST.has_key(u'IDcard'):
			IDcard = request.POST[u'IDcard'].encode('utf-8')
		if request.POST.has_key(u'phone'):
			phone = request.POST[u'phone'].encode('utf-8')

		if SecurityID == "" or name == "" or IDcard == "" or phone == "":
			context['result'] = "请填写全部信息！"
			return render(request, 'closeSecurityAccount.html',context)
		else:
			dictTmp['SecurityID'] = SecurityID
			dictTmp['name'] = name
			dictTmp['IDcard'] = IDcard
			dictTmp['phone'] = phone
			#以下均为临时数据
			dictTmp['gender'] = "1"
			dictTmp['address'] = "initial"
			dictTmp['career'] = "initial"
			dictTmp['education'] = "initial"
			dictTmp['company'] = "initial"
			dictTmp['StuffID']="inital"
			dictTmp['StuddName']="inital"
			dictTmp['password']="inital"
			dictTmp['AccountID']="inital"
			dictTmp['Balance']=0
			dictTmp['Password']="inital"
			dictTmp['BuyPassword']="inital"
			dictTmp['AccountID']="inital"
			dictTmp['Username']="inital"
			dictTmp['IsFreeze']="inital"
			print "test1"

			#创建临时数据
			userData = UserForm(dictTmp)
			print userData
			if userData.is_valid():
				userDataTMP = UserTable.objects.filter(SecurityID=SecurityID,IDcard=IDcard)
				print "test2"
				if(len(userDataTMP)):
					userTmp = userDataTMP[0]
					print "test3"
					if userTmp.compSecurityAccount(SecurityID,name,IDcard,phone):
						userTmp.delete()
		 	   	 		print "success!"
		 	   	 		context['result'] = "删除成功！"
						return render(request, 'closeSecurityAccount.html',context)
		 	   	 	else:
		 	   	 		context['result'] = "请输入正确的姓名和电话！"
						return render(request, 'closeSecurityAccount.html',context)
				else:
					context['result'] = "并无对应的证券账户和资金账户！"
					return render(request, 'closeSecurityAccount.html',context)

	return render(request, 'closeSecurityAccount.html',context)

@csrf_exempt
def closeCA(request):
	context = {}
	context['name'] = request.session.get('sessionname',default=None)
	context['state'] = request.session.get('sessionstate',default=None)
	context['img'] = request.session.get('sessionimage',default=None)
	request.encoding='utf-8'

	# 标志位
	tmp = ""

	SecurityID = ""
	CapitalID = ""
	username = ""
	IDcard = ""
	
	context['result'] = 'initial'
	#用于存放生成信息的词典
	dictTmp = {}

	if request.POST:
		if request.POST.has_key(u'SecurityID'):
			SecurityID = request.POST[u'SecurityID'].encode('utf-8')
		if request.POST.has_key(u'CapitalID'):
			CapitalID = request.POST[u'CapitalID'].encode('utf-8')
		if request.POST.has_key(u'IDcard'):
			IDcard = request.POST[u'IDcard'].encode('utf-8')
		if request.POST.has_key(u'username'):
			username = request.POST[u'username'].encode('utf-8')

		if SecurityID == "" or CapitalID == "" or username=="" or IDcard == "":
			tmp=1
		else:
			dictTmp['SecurityID'] = SecurityID
			dictTmp['IDcard'] = IDcard
			dictTmp['username']="inital"
			dictTmp['CapitalID']=CapitalID
			dictTmp['login_passwd']="inital"
			dictTmp['trans_passwd']="inital"
			dictTmp['confirm_loginPasswd']="inital"
			dictTmp['confirm_transPasswd']="inital"
			dictTmp['IsFreeze']=0
			dictTmp['phone'] = "initial"
			dictTmp['name'] = "initial"
			dictTmp['gender'] = "1"
			dictTmp['address'] = "initial"
			dictTmp['career'] = "initial"
			dictTmp['education'] = "initial"
			dictTmp['company'] = "initial"
			#创建临时数据
			capData = CapForm(dictTmp)
			print capData
			if capData.is_valid():
				capDataTMP = UserTable.objects.filter(SecurityID=SecurityID,IDcard=IDcard,AccountID=CapitalID)
				if(len(capDataTMP)):
					userTmp = capDataTMP[0]
					if userTmp.compPasswdInfo(SecurityID,IDcard,CapitalID):
						userTmp.delete()
						tmp=2

		if tmp == 1:
			message = "请将信息填写完整！"
		if tmp == 2:
			message = "注销成功！"
		# if tmp == 3:
		# 	message = "注销失败！"
		# 最好是返回失败的原因

		context['result'] = message

	return render(request, 'closeCapitalAccount.html', context)

@csrf_exempt
def operation(request):#存取款
	context = {}
	context['name'] = request.session.get('sessionname',default=None)
	context['state'] = request.session.get('sessionstate',default=None)
	context['img'] = request.session.get('sessionimage',default=None)
	request.encoding='utf-8'

	# 标志位
	tmp = "" #给出错误提示
	opera = "" #选择操作的类型 deposit or withdraw

	# deposit initial
	SecurityID1 = ""
	CapitalID1 = ""
	username1 = ""
	IDcard1 = ""
	balance1 = ""
	trans_passwd1 = ""
	confirm_transPasswd1 = ""

	# withdraw initial
	SecurityID2 = ""
	CapitalID2 = ""
	username2 = ""
	IDcard2 = ""
	balance2 = ""
	trans_passwd2 = ""
	confirm_transPasswd2 = ""
	message = ""
		#用于存放生成信息的词典
	dictTmp = {}

	context['result'] = 'initial'
	if request.POST:
		# deposit
		if request.POST.has_key(u'SecurityID1'):
			SecurityID1 = request.POST[u'SecurityID1'].encode('utf-8')
		if request.POST.has_key(u'CapitalID1'):
			CapitalID1 = request.POST[u'CapitalID1'].encode('utf-8')
		if request.POST.has_key(u'IDcard1'):
			IDcard1 = request.POST[u'IDcard1'].encode('utf-8')
		if request.POST.has_key(u'username1'):
			username1 = request.POST[u'username1'].encode('utf-8')
		if request.POST.has_key(u'balance1'):
			balance1 = request.POST[u'balance1'].encode('utf-8')
		if request.POST.has_key(u'trans_passwd1'):
			trans_passwd1 = request.POST[u'trans_passwd1'].encode('utf-8')
		if request.POST.has_key(u'confirm_transPasswd1'):
			confirm_transPasswd1 = request.POST[u'confirm_transPasswd1'].encode('utf-8')

		# withdraw
		if request.POST.has_key(u'SecurityID2'):
			SecurityID2 = request.POST[u'SecurityID2'].encode('utf-8')
		if request.POST.has_key(u'CapitalID2'):
			CapitalID2 = request.POST[u'CapitalID2'].encode('utf-8')
		if request.POST.has_key(u'IDcard2'):
			IDcard2 = request.POST[u'IDcard2'].encode('utf-8')
		if request.POST.has_key(u'username2'):
			username2 = request.POST[u'username2'].encode('utf-8')
		if request.POST.has_key(u'balance2'):
			balance2 = request.POST[u'balance2'].encode('utf-8')
		if request.POST.has_key(u'trans_passwd2'):
			trans_passwd2 = request.POST[u'trans_passwd2'].encode('utf-8')
		if request.POST.has_key(u'confirm_transPasswd2'):
			confirm_transPasswd2 = request.POST[u'confirm_transPasswd2'].encode('utf-8')

		if SecurityID1 != "" or CapitalID1 != "" or username1 != "" or IDcard1 != "" or balance1 != "" or trans_passwd1 != "" or confirm_transPasswd1 != "":
			opera = 1
		if SecurityID2 != "" or CapitalID2 != "" or username2 != "" or IDcard2 != "" or balance2 != "" or trans_passwd2 != "" or confirm_transPasswd2 != "":
			opera = 2
		
		if opera == 1:
			if SecurityID1 == "" or CapitalID1 == "" or username1 =="" or IDcard1 == "" or balance1 == "" or trans_passwd1 == "" or confirm_transPasswd1 == "":
				tmp = 1
			else:
				if trans_passwd1 != confirm_transPasswd1:
					tmp = 2
				# 此处加入代码
				# 判断输入的balance 和数据库中资金账户的余额
				# 做出判断
				# 给出相应的提示信息
				else:
					dictTmp['SecurityID'] = SecurityID1
					dictTmp['name'] = "initial"
					dictTmp['IDcard'] = IDcard1
					dictTmp['phone'] = "initial"
					#以下均为临时数据
					dictTmp['gender'] = "1"
					dictTmp['address'] = "initial"
					dictTmp['career'] = "initial"
					dictTmp['education'] = "initial"
					dictTmp['company'] = "initial"
					dictTmp['StuffID']="inital"
					dictTmp['StuddName']="inital"
					dictTmp['password']="inital"
					dictTmp['AccountID']=CapitalID1
					dictTmp['Balance']=balance1
					dictTmp['Password']="inital"
					dictTmp['BuyPassword']=trans_passwd1
					dictTmp['Username']=username1
					dictTmp['IsFreeze']=1
					#创建临时数据
					userData = UserForm(dictTmp)
					if userData.is_valid():
						#useru=UserTable.objects.all()
						#print useru
	
						#bbtmp= UserTable.objects.get(SecurityID=SecurityID1).values('Balance')
						#u_dict = model_to_dict(bbtmp) 
						us=UserTable()
						bbtmp=UserTable.objects.filter(SecurityID=SecurityID1).values("Balance")


						aa=UserTable.objects.filter(SecurityID=SecurityID1).values_list("Balance")
						 
				
						print type(bbtmp)
						print type(aa)
						print bbtmp
						print aa
						print "-----------------------------"

						userDataTMP = UserTable.objects.filter(SecurityID=SecurityID1,IDcard=IDcard1,AccountID=CapitalID1)
						if(len(userDataTMP)):
							userTmp = userDataTMP[0]
							if userTmp.compPasswdInfo(SecurityID1,IDcard1,CapitalID1):
								balance1 += bbtmp
								UserTable.objects.filter(SecurityID=SecurityID1,IDcard=IDcard1,AccountID=CapitalID1).update(ActiveMoney=balance1)
								tmp = 3
								#print userdatam
								#UserTable.objects.filter(SecurityID=SecurityID1,IDcard=IDcard1,AccountID=CapitalID1).update(Balance=)
								#print userDataTMP
								#addtmp=userDataTMP.objects.get(Balance)
								#if(addtmp >=balance1):
								#	addtmp={{addtmp|add:-balance1}}
								#	addtmp.save()
								#	print addtmp
							else:
								message="存款失败！"
					
		
		if opera == 2:
			if SecurityID2 == "" or CapitalID2 == "" or username2 =="" or IDcard2 == "" or balance2 == "" or trans_passwd2 == "" or confirm_transPasswd2 == "":
				tmp = 4
			else:
				if trans_passwd2 != confirm_transPasswd2:
					tmp = 5
				# 此处加入代码
				# 判断输入的balance 和数据库中资金账户的余额
				# 做出判断
				# 给出相应的提示信息
				else :
					dictTmp['SecurityID'] = SecurityID2
					dictTmp['name'] = "initial"
					dictTmp['IDcard'] = IDcard2
					dictTmp['phone'] = "initial"
					#以下均为临时数据
					dictTmp['gender'] = "1"
					dictTmp['address'] = "initial"
					dictTmp['career'] = "initial"
					dictTmp['education'] = "initial"
					dictTmp['company'] = "initial"
					dictTmp['StuffID']="inital"
					dictTmp['StuddName']="inital"
					dictTmp['password']="inital"
					dictTmp['AccountID']=CapitalID2
					dictTmp['Balance']=balance2
					dictTmp['Password']="inital"
					dictTmp['BuyPassword']=trans_passwd2
					dictTmp['Username']=username2
					dictTmp['IsFreeze']=1
					#创建临时数据
					userData = UserForm(dictTmp)
					if userData.is_valid():
						#useru=UserTable.objects.all()
						#print useru
	
						#bbtmp= UserTable.objects.get(SecurityID=SecurityID1).values('Balance')
						#u_dict = model_to_dict(bbtmp) 
						us=UserTable()
						bbtmp=UserTable.objects.filter(SecurityID=SecurityID1).values("Balance")

						# aa=UserTable.objects.filter(SecurityID=SecurityID1).values_list("Balance")
						# int(aa)
						print type(bbtmp)
						# print type(aa)
						print bbtmp
						# print aa
						print "-----------------------------"

						userDataTMP = UserTable.objects.filter(SecurityID=SecurityID2,IDcard=IDcard2,AccountID=CapitalID2)
						if(len(userDataTMP)):
							userTmp = userDataTMP[0]
							if userTmp.compPasswdInfo(SecurityID2,IDcard2,CapitalID2):
								balance2 -= bbtmp
								if balance2 < 0:
									message = "没有足够的余额取出！"
								else:
									UserTable.objects.filter(SecurityID=SecurityID2,IDcard=IDcard2,AccountID=CapitalID2).update(ActiveMoney=balance2)
									tmp = 3
								#print userdatam
								#UserTable.objects.filter(SecurityID=SecurityID1,IDcard=IDcard1,AccountID=CapitalID1).update(Balance=)
								#print userDataTMP
								#addtmp=userDataTMP.objects.get(Balance)
								#if(addtmp >=balance1):
								#	addtmp={{addtmp|add:-balance1}}
								#	addtmp.save()
								#	print addtmp
							else:
								message="取款失败！"
				
		if tmp == 1:
		 	message = "请将信息填写完整1 ！"
		if tmp == 2:
		 	message = "两次输入的交易密码不一致1 ！"
		if tmp == 3:
			message = "存款成功！"
		
		if tmp == 4:
		 	message = "请将信息填写完整2 ！"
		if tmp == 5:
		 	message = "两次输入的交易密码不一致2 ！"
		if tmp == 6:
		 	message = "取款成功！"

		context['result'] = message
	return render(request, 'operation.html', context)

@csrf_exempt
def changePassword(request):#改密码
	context = {}
	context['name'] = request.session.get('sessionname',default=None)
	context['state'] = request.session.get('sessionstate',default=None)
	context['img'] = request.session.get('sessionimage',default=None)
	request.encoding='utf-8'

	# 标志位
	tmp="" #给出提示

	psswd = "" #判断是login 还是transaction

	# login initial
	SecurityID1 = ""
	CapitalID1 = ""
	username1 = ""
	IDcard1 = ""
	oldLoginPasswd = ""
	newLoginPasswd = ""
	confirm_loginPasswd = ""

	# transaction initial
	SecurityID2 = ""
	CapitalID2 = ""
	username2 = ""
	IDcard2 = ""
	oldTransPasswd = ""
	newTransPasswd = ""
	confirm_transPasswd = ""
	message = ""

	context['result'] = 'initial'
		#用于存放生成信息的词典
	dictTmp = {}

	if request.POST:
		# 登录密码
		if request.POST.has_key(u'SecurityID1'):
			SecurityID1 = request.POST[u'SecurityID1'].encode('utf-8')
		if request.POST.has_key(u'CapitalID1'):
			CapitalID1 = request.POST[u'CapitalID1'].encode('utf-8')
		if request.POST.has_key(u'IDcard1'):
			IDcard1 = request.POST[u'IDcard1'].encode('utf-8')
		if request.POST.has_key(u'username1'):
			username1 = request.POST[u'username1'].encode('utf-8')
		if request.POST.has_key(u'oldLoginPasswd'):
			oldLoginPasswd = request.POST[u'oldLoginPasswd'].encode('utf-8')
		if request.POST.has_key(u'newLoginPasswd'):
			newLoginPasswd = request.POST[u'newLoginPasswd'].encode('utf-8')
		if request.POST.has_key(u'confirm_loginPasswd'):
			confirm_loginPasswd = request.POST[u'confirm_loginPasswd'].encode('utf-8')

		# 交易密码
		if request.POST.has_key(u'SecurityID2'):
			SecurityID2 = request.POST[u'SecurityID2'].encode('utf-8')
		if request.POST.has_key(u'CapitalID2'):
			CapitalID2 = request.POST[u'CapitalID2'].encode('utf-8')
		if request.POST.has_key(u'IDcard2'):
			IDcard2 = request.POST[u'IDcard2'].encode('utf-8')
		if request.POST.has_key(u'username2'):
			username2 = request.POST[u'username2'].encode('utf-8')
		if request.POST.has_key(u'oldTransPasswd'):
			oldTransPasswd = request.POST[u'oldTransPasswd'].encode('utf-8')
		if request.POST.has_key(u'newTransPasswd'):
			newTransPasswd = request.POST[u'newTransPasswd'].encode('utf-8')
		if request.POST.has_key(u'confirm_transPasswd'):
			confirm_transPasswd = request.POST[u'confirm_transPasswd'].encode('utf-8')

		if SecurityID1 != "" or CapitalID1 != "" or username1 != "" or IDcard1 != "" or oldLoginPasswd != "" or newLoginPasswd != "" or confirm_loginPasswd != "":
			passwd = 1
		if SecurityID2 != "" or CapitalID2 != "" or username2 != "" or IDcard2 != "" or oldTransPasswd != "" or newTransPasswd != "" or confirm_transPasswd != "":
			passwd = 2

		if passwd == 1:
			if SecurityID1 == "" or CapitalID1 == "" or username1 == "" or IDcard1 == "" or oldLoginPasswd == "" or newLoginPasswd =="" or confirm_loginPasswd =="":
				tmp = 1
			else :
				if oldLoginPasswd == newLoginPasswd:
					tmp = 2
				if newLoginPasswd != confirm_loginPasswd:
					tmp = 3
				if oldLoginPasswd != newLoginPasswd:
					if newLoginPasswd == confirm_loginPasswd:
						dictTmp['SecurityID'] = SecurityID1
						dictTmp['name'] = "inital"
						dictTmp['IDcard'] = IDcard1
						dictTmp['phone'] = "inital"
						#以下均为临时数据
						dictTmp['gender'] = "1"
						dictTmp['address'] = "initial"
						dictTmp['career'] = "initial"
						dictTmp['education'] = "initial"
						dictTmp['company'] = "initial"
						dictTmp['StuffID']="inital"
						dictTmp['StuddName']="inital"
						dictTmp['password']="inital"
						dictTmp['AccountID']=CapitalID1
						dictTmp['Balance']=0
						dictTmp['Password']="inital"
						dictTmp['BuyPassword']="inital"
						dictTmp['Username']=username1
						dictTmp['IsFreeze']="inital"
						#创建临时数据
						userData = UserForm(dictTmp)
						if userData.is_valid():
							userDataTMP = UserTable.objects.filter(SecurityID=SecurityID1,IDcard=IDcard1,AccountID=CapitalID1)
							if(len(userDataTMP)):
								userTmp = userDataTMP[0]
								if userTmp.compPasswdInfo(SecurityID1,IDcard1,CapitalID1):
									UserTable.objects.filter(SecurityID=SecurityID1,IDcard=IDcard1,AccountID=CapitalID1).update(Password=newLoginPasswd)
									tmp = 4 


						


		if passwd == 2:
			if SecurityID2 == "" or CapitalID2 == "" or username2 == "" or IDcard2 == "" or oldTransPasswd == "" or newTransPasswd =="" or confirm_transPasswd =="":
				tmp = 5
			else :
				if oldTransPasswd == newTransPasswd:
					tmp = 6
				if newTransPasswd == confirm_transPasswd:
					tmp = 7
				if oldTransPasswd != newTransPasswd:  
					if newTransPasswd == confirm_transPasswd:
						dictTmp['SecurityID'] = SecurityID2
						dictTmp['name'] = "inital"
						dictTmp['IDcard'] = IDcard2
						dictTmp['phone'] = "inital"
						#以下均为临时数据
						dictTmp['gender'] = "1"
						dictTmp['address'] = "initial"
						dictTmp['career'] = "initial"
						dictTmp['education'] = "initial"
						dictTmp['company'] = "initial"
						dictTmp['StuffID']="inital"
						dictTmp['StuddName']="inital"
						dictTmp['password']="inital"
						dictTmp['AccountID']=CapitalID2
						dictTmp['Balance']=0
						dictTmp['Password']="inital"
						dictTmp['BuyPassword']="inital"
						dictTmp['Username']=username2
						dictTmp['IsFreeze']="inital"
						#创建临时数据
						userData = UserForm(dictTmp)
						if userData.is_valid():
							userDataTMP = UserTable.objects.filter(SecurityID=SecurityID2,IDcard=IDcard2,AccountID=CapitalID2)
							if(len(userDataTMP)):
								userTmp = userDataTMP[0]
								if userTmp.compPasswdInfo(SecurityID2,IDcard2,CapitalID2):
									UserTable.objects.filter(SecurityID=SecurityID2,IDcard=IDcard2,AccountID=CapitalID2).update(BuyPassword=newTransPasswd)
									tmp = 8
						
		print SecurityID1
		print CapitalID1
		print username1
		print IDcard1
		print oldLoginPasswd
		print newLoginPasswd
		print confirm_loginPasswd

		print SecurityID2
		print CapitalID2
		print username2
		print IDcard2
		print oldTransPasswd
		print newTransPasswd
		print confirm_transPasswd


		if tmp == 1:
			message = "请将信息填写完整1 ！"
		if tmp == 2:
			message = "旧登录密码和新登录密码一致！"
		if tmp == 3:
			message = "两次输入的登录密码不一致1 ！"
		if tmp == 4:
			message = "登录密码修改成功！"
		
		# print tmp
		# print newTransPasswd
		# print confirm_transPasswd
	

		if tmp == 5:
			message = "请将信息填写完整2 ！"
		if tmp == 6:
			message = "旧交易密码和新交易密码一致！"
		if tmp == 7:
			message = "两次输入的交易密码不一致2 ！"
		if tmp == 8:
			message = "交易密码修改成功！"


		context['result'] = message

	return render(request, 'changePassword.html', context)

