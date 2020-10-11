from django.contrib.auth import views as auth_views
from django.urls import path

from .views import *

urlpatterns = [
    path('create_order/<int:pk>/', createOrder, name="create_order"),
    path('update_order/<int:pk>/', updateOrder, name="update_order"),
    path('delete_order/<int:pk>/', deleteOrder, name="delete_order"),
    path('customer/<int:pk>/', customers, name="customer"),

    path('reset_password/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/set_password.html"), name="password_reset_confirm"),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordChangeDoneView.as_view(template_name="accounts/password_reset_sent.html"), name="password_reset_done"),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), name="password_reset_complete"),

    path('user/', user_dashboard, name="user"),
    path('account/', accountSettings, name="account_settings"),
    path('register/', registerPage, name="register"),
    path('login/', loginPage, name="login"),
    path('logout/', logoutUser, name="logout"),
    path('contact/', contact, name="contact"),
    path('products/', products, name="products"),
    path('', home, name="home"),
]