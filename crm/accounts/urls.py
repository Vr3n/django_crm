from django.urls import path
from .views import home, contact, products, customers

urlpatterns = [
    path('', home, name="home"),
    path('contact/', contact, name="contact"),
    path('products/', products, name="products"),
    path('customer/<int:pk>/', customers, name="customers"),
]