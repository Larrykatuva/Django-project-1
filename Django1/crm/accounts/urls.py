from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', views.loginPage, name='login'),
    path('register', views.registerPage, name='register'),
    path('logout/', views.logoutPage, name='logout'),

    path('profile/', views.profile, name='products'),
    path('customer/<int:pk>/', views.customer, name='customer'),
    path('create_order/<int:pk>', views.create_order, name='create_order'),
    path('update_order/<int:pk>/', views.updateOrder, name='update_order'),
    path('delete_order/<int:pk>/', views.deleteOrder, name='delete_order'),
]