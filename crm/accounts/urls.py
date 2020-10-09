from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('contact/', contact, name="contact"),
    path('products/', products, name="products"),
    path('customer/<int:pk>/', customers, name="customer"),
    path('create_order/<int:pk>/', createOrder, name="create_order"),
    path('update_order/<int:pk>/', updateOrder, name="update_order"),
    path('delete_order/<int:pk>/', deleteOrder, name="delete_order"),
]