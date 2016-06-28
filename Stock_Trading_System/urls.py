"""Stock_Trading_System URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from Transaction_Client import views as Transaction_Client_views
# from central import views as central_views
from userAccount import views as userAccount_views
from manageStock import views as manageStock_views

urlpatterns = [
    url(r'^$', 'login.views.index', name='login'),
    #example
    url(r'^admin/', admin.site.urls),
    #Transaction Client
    url(r'^TransactionClient/$', Transaction_Client_views.login, name = 'Tran_login'),
     url(r'^TransactionClient/logout', Transaction_Client_views.logout, name = 'Tran_logout'),
    url(r'^TransactionClient/check/', Transaction_Client_views.check, name = 'Tran_check'),
    url(r'^TransactionClient/password/', Transaction_Client_views.password, name='password'),
    url(r'^TransactionClient/capital/', Transaction_Client_views.capital, name='capital'),
    url(r'^TransactionClient/possessed/', Transaction_Client_views.possessed, name='possessed'),
    url(r'^TransactionClient/stock/', Transaction_Client_views.stock, name='stock'),
    url(r'^TransactionClient/transaction/', Transaction_Client_views.transaction, name='transaction'),
    url(r'^TransactionClient/purchase/', Transaction_Client_views.purchase, name='purchase'),
    url(r'^TransactionClient/sell/', Transaction_Client_views.sell, name='sell'),
    url(r'^TransactionClient/faq/', Transaction_Client_views.faq, name='faq'),
    url(r'^TransactionClient/unlogin/', Transaction_Client_views.unlogin, name='unlogin'),
	url(r'^TransactionClient/search/', Transaction_Client_views.search, name='search'),    

	url(r'^TransactionClient/purchaseStock/', Transaction_Client_views.purchase_stock, name='purchase_stock'),
    url(r'^TransactionClient/purchase_stock_id_check/', Transaction_Client_views.purchase_stock_id_check, name='purchase_stock_id_check'),
    url(r'^TransactionClient/sellStock/', Transaction_Client_views.sell_stock, name='sell_stock'),
    url(r'^TransactionClient/sell_stock_id_check/', Transaction_Client_views.sell_stock_id_check, name='sell_stock_id_check'),
 

    url(r'^TransactionClient/modipasswd/', Transaction_Client_views.modipasswd, name='modipasswd'),
	# #Central Trading System
	# #init
	# url(r'^init/',central_views.initial),
	# #InsertTest
	# url(r'^insert/',central_views.insert),




    # user Account
    url(r'^userAccount/$', userAccount_views.login, name = 'userAccount_login'),
    # url(r'^userAccount/logout/', userAccount_views.logout, name = 'userAccount_logout'),

    url(r'^userAccount/homepage/', userAccount_views.homepage, name='userAccount_homepage'),
    #open
    url(r'^userAccount/openSecurityAccount/', userAccount_views.openSA, name='userAccount_openSecurityAccount'),
    url(r'^userAccount/openCapitalAccount/', userAccount_views.openCA, name='userAccount_openCapitalAccount'),

    #report The Loss
    url(r'^userAccount/reportSecurityLoss/', userAccount_views.reportSecurityLoss, name='userAccount_reportSecurityLoss'),
    url(r'^userAccount/reportCapitalLoss/', userAccount_views.reportCapitalLoss, name='userAccount_reportCapitalLoss'),

    #resubmit
    url(r'^userAccount/resubmitSecurityAccount/', userAccount_views.resubmitSA, name='userAccount_resubmitSecurityAccount'),
    url(r'^userAccount/resubmitCapitalAccount/', userAccount_views.resubmitCA, name='userAccount_resubmitCapitalAccount'),    

    #close an account
    url(r'^userAccount/closeSecurityAccount/', userAccount_views.closeSA, name='userAccount_closeSurityAccount'),
    url(r'^userAccount/closeCapitalAccount/', userAccount_views.closeCA, name='userAccount_closeCapitalAccount'),

    # operation  (deposit or withdraw)
    url(r'^userAccount/operation/', userAccount_views.operation, name='userAccount_operation'),

    # change password(include login password and transaction password)
    url(r'^userAccount/changePassword/', userAccount_views.changePassword, name='userAccount_changePassword'),    
     
# Manage Stocks
    url(r'^Manage/getStockInfo/', manageStock_views.GetStockInfo, name = 'getStockInfo'),
    url(r'^Manage/getStockList/', manageStock_views.GetStockList, name = "getStockList"),
    url(r'^Manage/freeze/', manageStock_views.FreezeStock, name = 'freezeStock'),
    url(r'^Manage/resume/', manageStock_views.RemuseStock, name = 'resumeStock'),
    url(r'^Manage/setLimit/', manageStock_views.SetLimit, name ='setLimit'),
    url(r'^Manage/', manageStock_views.home, name = 'manage_home'),

]

urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
