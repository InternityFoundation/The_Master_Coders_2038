from django.contrib import admin
from django.contrib.auth.models import Group
# Register your models here.

from .models import Hostel
from . models import available_items
from . models import User
from . models import student
from . models import *



class itemsadmin(admin.ModelAdmin):
	list_display = ('id','Hostel','item_name','price','hostel_num','quantity')
	list_editable = ('price','quantity',)
	list_per_page = 10
	search_fields = ('Hostel','item_name','price')
	list_filter = ('Hostel','price',)

class HostelAdmin(admin.ModelAdmin):
	list_display = ('id','hostel_num','name')
	list_per_page = 10
	search_fields = ('name','hostel_num')

class studentadmin(admin.ModelAdmin):
	list_display = ('user','name','email','phone','balance',)
	list_editable = ('balance','name','email','phone')
	list_per_page = 10
	search_fields = ('user',)
	
class properorderadmin(admin.ModelAdmin):
	list_display = ('order_client','order_timestamp','order_price','order_done',)
	list_per_page = 100
class itemorderadmin(admin.ModelAdmin):
	list_display = ('in_order','already_ordered','add_by','price','hostell',)
	list_per_page = 10


admin.site.register(Hostel,HostelAdmin)
admin.site.register(available_items,itemsadmin)
admin.site.register(student,studentadmin)

admin.site.register(ProperOrder,properorderadmin)
admin.site.register(Item,itemorderadmin)

