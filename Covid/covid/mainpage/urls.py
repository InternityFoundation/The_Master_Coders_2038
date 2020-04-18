from django.urls import path,include
from . import views
from app.views import add_to_cart,mark_order_as_done
urlpatterns=[
    path('',views.masterhome,name="master_home"),
    path('hcs/',include('homepage.urls')),
    path('mcms/',include('app.urls')),
    path('add/<str:item_type>/<int:item_id>/<int:hostel_num>', add_to_cart, name="add_to_cart"),
    path("order/<int:order_id>/done",mark_order_as_done, name="mark_order_as_done"),
    path('about/',views.about,name="about"),
]
