from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
urlpatterns=[
	
    path('signup',views.signup,name='signup'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('forgot',views.forgot,name='forgot'),
    path('details',views.details,name='details'),
    
]
