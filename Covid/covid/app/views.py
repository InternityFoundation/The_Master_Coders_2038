from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from .models import Hostel,available_items,student
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required,permission_required
from .models import *
from datetime import date

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
               	return HttpResponseRedirect(reverse('mcms_home'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'login.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('mcms_home'))

@login_required
def home(request):
	context = {}
	context.update({'Hostel':Hostel.objects.all()})
	context.update({'orders': reversed(ProperOrder.objects.filter(hos=request.user))})
	return render(request,'index.html',context)

@login_required
def account(request):
	context = {
		'student':student.objects.filter(user=request.user)
		}
	return render(request,'myaccount.html',context)


@login_required
def menutoday(request,hostel):
	context = {
		'menu':available_items.objects.filter(Hostel=hostel)
		}
	return render(request,'menu_today.html',context)

def calculate_cart_price(username):
    price_all = 0
    for obj in Item.objects.filter(add_by=username).filter(already_ordered=False):
        price_all += obj.price*obj.quantity
    return price_all

@login_required
def menu(request,hostel_num):
	for obj in Item.objects.filter(add_by=request.user).filter(already_ordered=False):
		if(obj.itemtype.hostel_num!=hostel_num):
			delete_all_user_orders(request.user)
	context = {
		'menu':available_items.objects.filter(hostel_num=hostel_num)
		}
	return render(request,'menu.html',context)

@login_required
def cart(request):
    price_all = calculate_cart_price(request.user)
    context = {}
    context.update({"price_all": price_all})
    context.update({"Item": Item.objects.filter(add_by=request.user).filter(already_ordered=False)})
    update_total(request.user)
    return render(request, 'cart.html', context)

def update_total(username):
    items = Item.objects.filter(add_by=username).filter(already_ordered=False)
    for i in items:
    	i.total=i.price*i.quantity;
    	i.save()

def update_quantity(username,idss):
	qty=available_items.objects.filter(id=idss).get()
	i = Item.objects.filter(add_by=username).filter(already_ordered=False)
	for ii in i:
		if(ii.itemtype.id==idss and ii.quantity<qty.quantity):
			ii.quantity+=1;
		ii.save()

@login_required()
def add_to_cart(request, item_type, item_id,hostel_num):
    try:
        h=Hostel.objects.filter(hostel_num=hostel_num).get()
        i = Item.objects.filter(add_by=request.user).filter(already_ordered=False).get(itemtype=item_id)
    except Item.DoesNotExist:
        i =None
    if(i==None):
        item_id = available_items.objects.get(id=item_id)
        q=item_id.quantity
        if(q==0):
            messages.add_message(request, messages.INFO, "Item unavailable!")
            return redirect("menu",hostel_num)
        new_item = Item(itemtype=item_id,add_by=request.user,hostell=h.name)
        new_item.calculate_price()
        new_item.save()
        messages.add_message(request, messages.INFO, "Item added to cart!")
        return redirect("menu",hostel_num)
    messages.add_message(request, messages.INFO, "Item added to cart!")
    update_quantity(request.user,item_id)
    return redirect("menu",hostel_num)    

@login_required()
def make_order(request):
    h=Item.objects.filter(add_by=request.user).filter(already_ordered=False)[0]
    new_proper_order = ProperOrder(hos=h.hostell)
    stud=student.objects.get(user=request.user)
    new_proper_order.order_client = request.user
    new_proper_order.order_price = calculate_cart_price(request.user)
    if(new_proper_order.order_price==0):
    	messages.add_message(request, messages.INFO, "Please add something to place order !")
    elif(stud.balance>new_proper_order.order_price and new_proper_order.order_price!=0):
	    new_proper_order.save()
	    for item in Item.objects.filter(add_by=request.user).filter(already_ordered=False):
	        item.already_ordered = True
	        item.in_order = new_proper_order
	        item.save()
	        update_total_quantity(item.itemtype.id,item.quantity)
	    stud.balance=stud.balance-new_proper_order.order_price
	    balance=stud.balance
	    update_balance(request.user,balance)
	    messages.add_message(request, messages.INFO, "Order Placed Successfully!")    	
    else:
    	messages.add_message(request, messages.INFO, "Order Failed due to insufficient Wallet Balance !")
    return redirect(user_orders_view)	

def update_total_quantity(iddd,qty):
	for item in available_items.objects.all():
		if(item.id==iddd):
			item.quantity-=qty
		item.save()		

def update_balance(username,balance):
    stu=student.objects.get(user=username)
    stu.balance=balance;
    stu.save()

def delete_all_user_orders(username):
    Item.objects.filter(add_by=username).filter(already_ordered=False).delete() 
    return True

def delete_user_order(username,ids):
	Item.objects.filter(add_by=username).filter(already_ordered=False).filter(id=ids).delete() 

@login_required
def clear_cart(request):
    delete_all_user_orders(request.user)
    return redirect("cart")

@login_required
def remove_item(request,item_id):
	ids=0
	for obj in Item.objects.filter(add_by=request.user).filter(already_ordered=False):
		if(obj.itemtype.id==item_id):
			ids=obj.id
	delete_user_order(request.user,ids)
	return redirect("cart")

@login_required
def user_orders_view(request):
    context = {"orders": reversed(ProperOrder.objects.filter(order_client=request.user))}
    return render(request, 'my_orders.html', context)

@login_required
def mark_order_as_done(request, order_id):
    marked = ProperOrder.objects.get(id=order_id)
    marked.order_done = True
    marked.save()
    return redirect("mcms_home")
@login_required
def mcms_update(request,i):
    if request.GET:
        update_term = request.GET['update_term']   
        context = {
		'menu':available_items.objects.filter(Hostel=request.user)
		}
        qtyy= available_items.objects.get(id=i)
        qtyy.quantity=update_term
        qtyy.save()
        return render(request,'menu_today.html',context)


@login_required
def search(request):
    if request.GET:
        search_term = request.GET['search_term']

        context = {
            'search_term': search_term,
            'students': student.objects.filter(name=search_term)
        }
        return render(request, 'search.html', context)
    else:
        return redirect('mcms_home')

@login_required
def upbal(request,phone):
    if request.GET:
        update_term = request.GET['update_term']   
        bal= student.objects.get(phone=phone)
        bal.balance=bal.balance+int(update_term)
        bal.save()
        return redirect('mcms_home')
# {{ item.order_timestamp |timesince }}
def calculate_cart_price(username):
    price_all = 0
    for obj in Item.objects.filter(add_by=username).filter(already_ordered=False):
        price_all += obj.price*obj.quantity
    return price_all
def tots(username):
	total = 0

	for obj in ProperOrder.objects.filter(order_timestamp__date=date.today()).filter(hos=username):
		total+=obj.order_price
	return total
@login_required
def totalsale(request):
	context = {}
	total = tots(request.user)
	context.update({"total": total})
	return render(request,'total_sale.html',context)

