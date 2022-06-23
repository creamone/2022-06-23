from django.contrib import admin
from django.urls import path , include
from . import views

# url이 item인거
urlpatterns = [
    path('', views.ItemView.as_view()),
    path('order/', views.OrderView.as_view()),

]
