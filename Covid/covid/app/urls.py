from django.conf.urls import url
from django.urls import path
from . import views
urlpatterns = [
    url(r'^logout/$', views.user_logout, name='logout'),
	url(r'^user_login/$',views.user_login,name='user_login'),
	path('',views.home,name="mcms_home"),
	path('totalsale/',views.totalsale,name="totalsale"),
	path('menu/<int:hostel_num>',views.menu,name="menu"),
	path('myaccount/',views.account,name="account"),
	path('cart/',views.cart,name="cart"),
	path('search/', views.search, name="search"),
	path('upbal/<int:phone>', views.upbal, name="upbal"),
	path('mcms_update/<int:i>', views.mcms_update, name="mcms_update"),
	path('today/<str:hostel>',views.menutoday,name="menu_today"),
	path('add/<str:item_type>/<int:item_id>/<int:hostel_num>', views.add_to_cart, name="add_to_cart"),
    path('finalize/', views.make_order, name="make_order" ),
    path('my_orders/', views.user_orders_view, name="user_orders_view"),
    path('clear_cart/', views.clear_cart, name="clear_cart"),
    path('remove_item/<int:item_id>', views.remove_item, name="remove_item"),
    path('update_balance/', views.update_balance, name="update_balance"),
    path('update_quantity/', views.update_quantity, name="update_quantity"),
    path("order/<int:order_id>/done",views.mark_order_as_done, name="mark_order_as_done"),
]
