from django.urls import path
from . import views

urlpatterns = [
    path('newset/', views.createset, name='createset'),
    path('search/', views.search, name='search'),
    path('explore/', views.explore, name='explore'),
    path('explore/<str:selectedset>/', views.setdetail, name='setdetail'),
    path('set=<str:setname>/', views.cardlist, name='cardlist'),
    path('', views.home, name='home'),
]
