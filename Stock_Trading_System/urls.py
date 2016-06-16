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


]

urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
