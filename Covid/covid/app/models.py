from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import datetime

# Create your models here.

class student(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	balance = models.IntegerField(default=0)
	phone = models.IntegerField(default=0)
	name = models.CharField(max_length=20,default='student')
	email = models.EmailField(max_length=100,default='@thapar.edu')
	Hostel = models.ForeignKey('Hostel',on_delete=models.DO_NOTHING,default=1)

class available_items(models.Model):
	Hostel = models.CharField(max_length=20)
	item_name = models.CharField(max_length=20)
	price = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
	hostel_num = models.IntegerField(default=1)
	quantity = models.IntegerField(default=10)
	def __str__(self):
		return self.item_name

class Hostel(models.Model):
	name = models.CharField(max_length=20)
	hostel_num = models.IntegerField(default=1)
	def __str__(self):
		return self.name

class ProperOrder(models.Model):
    order_client = models.ForeignKey(User, on_delete=models.CASCADE)
    order_timestamp = models.DateTimeField(auto_now_add=True)
    order_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, editable=False)
    order_done = models.BooleanField(default=False)
    hos = models.CharField(max_length=10,null=True)
    def __str__(self):
        return self.id

class Item(models.Model):
    in_order = models.ForeignKey(ProperOrder, on_delete=models.CASCADE, null=True, blank=True, related_name="item")
    already_ordered = models.BooleanField(default=False)
    add_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    itemtype = models.ForeignKey(available_items, on_delete=models.CASCADE,null=True)
    price = models.DecimalField(max_digits=4, decimal_places=2, default=0.00, editable=False)
    quantity = models.IntegerField(default=1)
    hostell = models.CharField(max_length=10,null=True)
    total = models.DecimalField(max_digits=4, decimal_places=0, default=0.00, editable=False)
    def calculate_price(self):
    	self.price = self.itemtype.price
    def __str__(self):
        return self.in_order
