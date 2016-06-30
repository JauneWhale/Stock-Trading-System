# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.template import RequestContext
# from userAccount.models import UserTable
from userAccount.models import *
from django.http import HttpResponseRedirect
from database.models import *
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

#定义表单模型
class UserForm(forms.Form):
	SecurityID = forms.CharField(label='SecurityID：',max_length=20)
	IsFreeze = forms.IntegerField(label='IsFreeze:')
	name = forms.CharField(label='用户名：',max_length=20)
	IDcard = forms.CharField(label='IDcard:',max_length=20)
	phone = forms.CharField(label='phone:',max_length=20)
	gender = forms.IntegerField(label='gender:')
	address = forms.CharField(max_length=20)
	career = forms.CharField(label='career:',max_length=20)
	education = forms.CharField(label='education:',max_length=20)
	company = forms.CharField(label='company:',max_length=20)
	#IsFree = forms.CharField(label='IsFreeze:',max_length=20)
	
class CapForm(forms.Form):
	SecurityID = forms.CharField(label='SecurityID：',max_length=20)
	CapitalID=forms.CharField(max_length=20)
	# username=forms.CharField(max_length=20)
	IDcard = forms.CharField(label='IDcard:',max_length=20)
	name = forms.CharField(label='用户名：',max_length=20)
	IsTransFreeze = models.BooleanField(default=False)
	
	

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
			request.session['sessionid'] = staffid
		if request.POST.has_key(u'staffname'):
			staffname = request.POST[u'staffname'].encode('utf-8')
			request.session['sessionname'] = staffname
		if request.POST.has_key(u'password'):
			password = request.POST[u'password'].encode('utf-8')
		request.session['sessionstate'] = 'Administrator'
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
				if len(sfDataTMP) != 0:
					if staffid == sfDataTMP[0].StuffID and staffname == sfDataTMP[0].StuddName and password == sfDataTMP[0].Password:
						tmp = 2
					else:
						tmp = 1


				# if(len(sfDataTMP)):
				# 	sfTmp = sfDataTMP[0]
				# 	if sfTmp.compStuffID(staffid):
				# 		tmp = 2


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
	context['id'] = request.session.get('sessionid', default=None)
	context['name'] = request.session.get('sessionname',default=None)
	context['state'] = request.session.get('sessionstate',default=None)
	context['img'] = request.session.get('sessionimage',default=None)
	return render(request,'userHomepage.html',context)

	
@csrf_exempt
def openSA(request):
	context = {}
	context['id'] = request.session.get('sessionid', default=None)
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
	IsFreeze = 0

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

			if (SecurityID == "" or name == "" or IDcard == "" or phone=="" or gender == "" or address == "" or career == "" or education == "" or company == ""):
				tmp = 1

			else:
				tmp = 2
				 #将表单写入数据库
				user = UserTable()
				
				user.Name = name
				user.IDcard = IDcard
				user.Tel = phone
				user.Gender = gender
				user.HomeAddr = address
				user.Occupation = career
				user.EduInfo = education
				user.Department = company
				user.save()

				security = SecurityAccountInfo()

				security.SecurityID = SecurityID
				security.IDcard=user
				security.IsFreeze= IsFreeze 


				# user.save()
				security.save()

				print "test" 


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
	context['id'] = request.session.get('sessionid', default=None)
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
	ActiveMoney=0.0
	FrozenMoney = 0.0
	BankCard = 0

	
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
		elif len(login_passwd)<6:
			tmp = 6
		elif len(trans_passwd)<6:
			tmp = 6
		elif login_passwd != confirm_loginPasswd:
			tmp = 4
		elif trans_passwd != confirm_transPasswd:
			tmp = 5

		else:
			# UserTable.objects.filter(SecurityID=SecurityID,IDcard=IDcard).update(AccountID=CapitalID,ActiveMoney=0,BuyPassword=trans_passwd,Password=login_passwd,Username=username)
			ut = UserTable.objects.filter(IDcard=IDcard)
			if len(ut)!=0:
				sa = SecurityAccountInfo.objects.filter(SecurityID=SecurityID,IDcard=ut)
				if len(sa)!=0:
					tmp=2
					newca = CapitalAccountInfo()
					newca.AccountID = CapitalID
					newca.Password = login_passwd
					newca.UserTable = ut[0]
					newca.SecurityAccount = sa[0]
					newca.BuyPassword = trans_passwd
					newca.save()

					newci = CapitalInfo()
					newci.AccountID = CapitalID
					newci.ActiveMoney = ActiveMoney
					newci.FrozenMoney = FrozenMoney
					newci.BankCard = BankCard
					newci.save()
				else:
					tmp=3
			else:
				tmp=3

		if  tmp == 1 :
			message = "请将信息填写完整!"
		if tmp == 2 :
			message = "开通成功!"
		if tmp == 3:
			message = "不存在！"
		if tmp == 4:
			message = "两次输入的登录密码不一致！"
		if tmp == 5:
			message = "两次输入的交易密码不一致！"
		if tmp == 6:
			message = "密码的长度不够！"
		# if tmp == 3:
		# 	message = "开通失败！"
		# 最好是返回失败的原因
	
		context['result'] = message

	return render(request, 'openCapitalAccount.html', context)

@csrf_exempt
def reportSecurityLoss(request):
	context = {}
	context['id'] = request.session.get('sessionid', default=None)
	context['name'] = request.session.get('sessionname',default=None)
	context['state'] = request.session.get('sessionstate',default=None)
	context['img'] = request.session.get('sessionimage',default=None)
	request.encoding='utf-8'

	# 标志位
	tmp = ""

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

		if SecurityID == "" or IDcard == "" or name=="":
			context['result'] = "请填写全部信息！"
			return render(request, 'reportSecurityLoss.html',context)
		else:
			dictTmp['SecurityID'] = SecurityID
			dictTmp['name'] = name
			dictTmp['IDcard'] = IDcard
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
				ut = UserTable.objects.filter(IDcard=IDcard)

				if len(ut)!=0:
					sa = SecurityAccountInfo.objects.filter(SecurityID=SecurityID,IDcard=ut)
					if len(sa)!=0:
						if sa[0].IsFreeze==0:
							sa.update(IsFreeze=1)
							context['result'] = "挂失成功！"
						else:
							context['result'] = "该账户已挂失！"
					else:
						context['result'] = "未知错误1!"
				else:
					context['result'] = "未知错误2！"

	return render(request, 'reportSecurityLoss.html', context)

@csrf_exempt
def reportCapitalLoss(request):
	context = {}
	context['id'] = request.session.get('sessionid', default=None)
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
	IsTransFreeze=""

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
			context['result'] = "请将信息填写完整！"
			return render(request, 'reportSecurityLoss.html',context)
		else:
			
			dictTmp['SecurityID'] = SecurityID
			dictTmp['IDcard'] = IDcard
			dictTmp['name']=username
			dictTmp['CapitalID']=CapitalID
			dictTmp['IsTransFreeze'] = True
		

			#创建临时数据
			capData = CapForm(dictTmp)
			print capData
			if capData.is_valid():
				ut = UserTable.objects.filter(IDcard=IDcard)
				if len(ut) != 0:
					sa = SecurityAccountInfo.objects.filter(SecurityID=SecurityID,IDcard=ut[0])
					if len(sa) != 0:
						ca = CapitalAccountInfo.objects.filter(AccountID=CapitalID,SecurityAccount=sa[0],UserTable=ut[0])
						if ca[0].IsTransFreeze == False:
							ca.update(IsTransFreeze = True)
							context['result'] = "该资金账户挂失成功！"
						else:
							context['result'] = "该资金账户已挂失！"
					else:
						context['result'] = "未知错误1!"
				else:
					context['result'] = "未知错误2!"
			else:
				context['result'] = "未知错误3!"

		# if tmp == 3:
		# 	message = "挂失失败"
		# 最好是返回失败的原因

		#context['result'] = message

	return render(request, 'reportCapitalLoss.html', context)

@csrf_exempt
def resubmitSA(request):
	context = {}
	context['id'] = request.session.get('sessionid', default=None)
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
	# message = ""

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
			context['result'] = "请将信息填写完整！"
		else:
			
			dictTmp['SecurityID'] = SecurityID
			dictTmp['name'] = name
			dictTmp['IDcard'] = IDcard
			dictTmp['phone'] = phone
			#以下均为临时数据
			dictTmp['gender'] = gender
			dictTmp['address'] = address
			dictTmp['career'] = career
			dictTmp['education'] = education
			dictTmp['company'] = company
			dictTmp['IsFreeze']=1

			userData=UserForm(dictTmp)
			print userData
			# message = "IDcard不存在"
			if userData.is_valid():
				ut = UserTable.objects.filter(IDcard=IDcard)
				if len(ut) != 0:
					sa = SecurityAccountInfo.objects.get(IDcard=ut[0])
					sa.delete()
					sa.SecurityID = SecurityID
					sa.save()
					context['result'] = "补办成功！"
					# else:
					# 	context['result'] = "补1111111！"
				else:
					context['result'] = "补111111！"
			else:
				context['result'] = "补11111！"


		# context['result'] = message
	return render(request, 'resubmitSecurityAccount.html', context)

@csrf_exempt
def resubmitCA(request):
	context = {}
	context['id'] = request.session.get('sessionid', default=None)
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
			context['result'] = "请将信息填写完整！"
		else:
			
			context['result']="没有权限！"

	return render(request, 'resubmitCapitalAccount.html', context)

@csrf_exempt
def closeSA(request):
	context = {}
	context['id'] = request.session.get('sessionid', default=None)
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
			# dictTmp['Balance']=0
			dictTmp['Password']="inital"
			dictTmp['BuyPassword']="inital"
			dictTmp['AccountID']="inital"
			# dictTmp['Username']="inital"
			dictTmp['IsFreeze']=0
			print "test1"

			#创建临时数据
			userData = UserForm(dictTmp)
			print userData
			if userData.is_valid():
				ut = UserTable.objects.filter(IDcard=IDcard)
				if len(ut) != 0:
					sa = SecurityAccountInfo.objects.filter(SecurityID=SecurityID,IDcard=ut[0])
					if len(sa) != 0:
						CapitalAccountInfo.objects.filter(UserTable=ut[0], SecurityAccount=sa[0]).delete()
						sa.delete()
						ut.delete()
						context['result'] = "注销账户成功！"
					else:
						context['result'] = "未知错误1！"
				else:
						context['result'] = "未知错误2！"
			else:
				context['result'] = "未知错误3！"

	return render(request, 'closeSecurityAccount.html',context)

@csrf_exempt
def closeCA(request):
	context = {}
	context['id'] = request.session.get('sessionid', default=None)
	context['name'] = request.session.get('sessionname',default=None)
	context['state'] = request.session.get('sessionstate',default=None)
	context['img'] = request.session.get('sessionimage',default=None)
	request.encoding='utf-8'

	# 标志位
	tmp = ""

	SecurityID = ""
	CapitalID = ""
	username = ""
	message= ""
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
			context['result'] = "请将信息填写完整！"
		else:
			dictTmp['SecurityID'] = SecurityID
			dictTmp['IDcard'] = IDcard
            # dictTmp['username']="inital"
			dictTmp['CapitalID']=CapitalID
			dictTmp['name'] = username
			# dictTmp['trans_passwd']="inital"
			# dictTmp['login_passwd']="inital"
			# dictTmp['loginPwdWrongNum']="inital"
			# dictTmp['transPwdWrongNum']="inital"
			# dictTmp['lastTimeTrans']="inital"
			# dictTmp['lastTimeLogin']="inital"
			# dictTmp['IsTransFreeze']="inital"
			# dictTmp['IsLoginFreeze']="inital"
			# dictTmp['Isfirst']="inital"
			
			#创建临时数据
			capData = CapForm(dictTmp)
			print capData
			if capData.is_valid():
				ut = UserTable.objects.filter(IDcard=IDcard)
				if len(ut) != 0 :
					sa = SecurityAccountInfo.objects.filter(SecurityID=SecurityID,IDcard=ut[0])
					if len(sa) != 0:
						ca = CapitalAccountInfo.objects.filter(AccountID=CapitalID,SecurityAccount=sa[0],UserTable=ut[0])
						if len(ca) != 0:
							ca.delete()
							context['result'] = "资金账户注销成功！"
					else:
						context['result'] = "未知错误1！"
				else:
					context['result'] = "未知错误2！"
			else:
				context['result'] = "未知错误3！"


	return render(request, 'closeCapitalAccount.html', context)

@csrf_exempt
def operation(request):#存取款
	context = {}
	context['id'] = request.session.get('sessionid', default=None)
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
				context['result']="请将信息填写完整1！"
			else:
				if trans_passwd1 != confirm_transPasswd1:
					context['result']="两次输入的交易密码不一致1！"
			
				else:
					dictTmp['SecurityID'] = SecurityID1
					dictTmp['name'] = username1
					dictTmp['IDcard'] = IDcard1
					dictTmp['phone'] = "initial"
					dictTmp['IsTransFreeze']=True
					dictTmp['CapitalID']=CapitalID1
					# dictTmp['ActiveMoney']=0

					#创建临时数据
					userData = CapForm(dictTmp)
					print userData
					if userData.is_valid():
						ut = UserTable.objects.filter(IDcard=IDcard1)
						if len(ut) != 0:
							sa = SecurityAccountInfo.objects.filter(SecurityID=SecurityID1,IDcard=ut[0])
							if len(sa) != 0:
								ca = CapitalAccountInfo.objects.filter(AccountID=CapitalID1,SecurityAccount=sa[0],UserTable=ut[0])
								if len(ca) != 0:
									if ca[0].IsTransFreeze == True:
										context['result'] = "该资金账户已被锁定！无法进行交易！"
									else:
										ci = CapitalInfo.objects.get(AccountID=ca[0].AccountID)
										ci.ActiveMoney = ci.ActiveMoney + float(balance1)
										ci.save()
										print 12314134324
										print ca[0].AccountID
										context['result'] = "存款成功！"
								else:
									context['result'] = "hahahah111！"
							else:
								context['result'] = "22222！"
						else:
							context['result'] = "2333332！"
					else:
						context['result'] = "存4444！"

					
		
		if opera == 2:
			if SecurityID2 == "" or CapitalID2 == "" or username2 =="" or IDcard2 == "" or balance2 == "" or trans_passwd2 == "" or confirm_transPasswd2 == "":
				context['result']="请将信息填写完整2！"
			else:
				if trans_passwd2 != confirm_transPasswd2:
					context['result']="两次输入的交易密码不一致2！"
				# 此处加入代码
				# 判断输入的balance 和数据库中资金账户的余额
				# 做出判断
				# 给出相应的提示信息
				else:
					dictTmp['SecurityID'] = SecurityID2
					dictTmp['name'] = username2
					dictTmp['IDcard'] = IDcard2
					dictTmp['phone'] = "initial"
					dictTmp['IsTransFreeze']=True
					dictTmp['CapitalID']=CapitalID2

					#创建临时数据
					userData = CapForm(dictTmp)
					if userData.is_valid():
						ut = UserTable.objects.filter(IDcard=IDcard2)
						if len(ut) != 0:
							sa = SecurityAccountInfo.objects.filter(SecurityID=SecurityID2,IDcard=ut[0])
							if len(sa) != 0:
								ca = CapitalAccountInfo.objects.filter(AccountID=CapitalID2,SecurityAccount=sa[0],UserTable=ut[0])
								if len(ca) != 0:
									if ca[0].IsTransFreeze == True:
										context['result'] = "该资金账户已被锁定！无法进行交易！"
									else:
										ci = CapitalInfo.objects.get(AccountID=ca[0].AccountID)
										if ci.ActiveMoney < float(balance2):
											context['result'] = "余额不足！"
										else:
											ci.ActiveMoney = ci.ActiveMoney - float(balance2)
											ci.save()
											context['result'] = "取款成功！"

	return render(request, 'operation.html', context)


@csrf_exempt
def changePassword(request):#改密码
	context = {}
	context['id'] = request.session.get('sessionid', default=None)
	context['name'] = request.session.get('sessionname',default=None)
	context['state'] = request.session.get('sessionstate',default=None)
	context['img'] = request.session.get('sessionimage',default=None)
	request.encoding='utf-8'


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

	# message = ""

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
				context['result'] = "请将信息填写完整1！"
			else :
				if oldLoginPasswd == newLoginPasswd:
					context['result'] = "新旧登录密码一致！"
				else:
					if newLoginPasswd != confirm_loginPasswd:
						context['result'] = "两次输入的登录密码不一致！"
					else:
						dictTmp['SecurityID'] = SecurityID1
						dictTmp['name'] = username1
						dictTmp['IDcard'] = IDcard1
						dictTmp['phone'] = "initial"
						#以下均为临时数据
						dictTmp['gender'] = "1"
						dictTmp['address'] = "initial"
						dictTmp['career'] = "initial"
						dictTmp['education'] = "initial"
						dictTmp['company'] = "initial"
						dictTmp['AccountID']=CapitalID1
						dictTmp['Password']="inital"
						dictTmp['BuyPassword']="inital"
						dictTmp['IsFreeze']=1

						#创建临时数据
						userData = UserForm(dictTmp)
						if userData.is_valid():
							ut = UserTable.objects.filter(IDcard=IDcard1)
							if len(ut) != 0 :
								sa = SecurityAccountInfo.objects.filter(SecurityID=SecurityID1,IDcard=ut[0])
								if len(sa) !=0 :
									ca = CapitalAccountInfo.objects.filter(AccountID=CapitalID1,SecurityAccount=sa[0],UserTable=ut[0])
									if len(ca) != 0:
										ca.update(Password=newLoginPasswd)
										context['result'] = "登录密码修改成功！"
									else:
										context['result'] = "登录密码修改失败！"
								else:
									context['result'] = "未知错误1！"
							else:
								context['result'] = "未知错误2！"
						else:
							context['result'] = "未知错误3！"



		if passwd == 2:
			if SecurityID2 == "" or CapitalID2 == "" or username2 == "" or IDcard2 == "" or oldTransPasswd == "" or newTransPasswd =="" or confirm_transPasswd =="":
				context['result'] = "请将信息填写完整2！"
			else :
				if oldTransPasswd == newTransPasswd:
					context['result'] = "新旧交易密码一致！"
				else: 
					if newTransPasswd != confirm_transPasswd:
						context['result'] = "两次输入的交易密码不一致！"
					else:
						dictTmp['SecurityID'] = SecurityID2
						dictTmp['name'] = username2
						dictTmp['IDcard'] = IDcard2
						dictTmp['phone'] = "initial"
						#以下均为临时数据
						dictTmp['gender'] = "1"
						dictTmp['address'] = "initial"
						dictTmp['career'] = "initial"
						dictTmp['education'] = "initial"
						dictTmp['company'] = "initial"
						dictTmp['AccountID']=CapitalID2
						dictTmp['Password']="inital"
						dictTmp['BuyPassword']="inital"
						dictTmp['IsFreeze']=1

						#创建临时数据
						userData = UserForm(dictTmp)
						if userData.is_valid():
							ut = UserTable.objects.filter(IDcard=IDcard2)
							if len(ut) != 0 :
								sa = SecurityAccountInfo.objects.filter(SecurityID=SecurityID2,IDcard=ut[0])
								if len(sa) !=0 :
									ca = CapitalAccountInfo.objects.filter(AccountID=CapitalID2,SecurityAccount=sa[0],UserTable=ut[0])
									if len(ca) != 0:
										ca.update(BuyPassword=newTransPasswd)
										context['result'] = "交易密码修改成功！"
									else:
										context['result'] = "交易密码修改失败！"
								else:
									context['result'] = "未知错误1！"
							else:
								context['result'] = "未知错误2！"
						else:
							context['result'] = "未知错误3！"



	return render(request, 'changePassword.html', context)

