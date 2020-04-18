from django.urls import path,include
from . import views

urlpatterns=[
    path('',views.home,name="hcs_home"),
    path('complaints/',include('complaints.urls')),
]
