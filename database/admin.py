from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(UserTable)
admin.site.register(SecurityAccountInfo)
admin.site.register(CapitalAccountInfo)
admin.site.register(InstDealed)
admin.site.register(StockInfo)
admin.site.register(CapitalInfo)
admin.site.register(SecurityStockInfo)

