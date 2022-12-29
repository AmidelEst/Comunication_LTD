from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .forms import *

from . import views
app_name = 'interface'

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('login', views.login2, name='login'),
    path('logout', views.logoutView, name='logout'),
    path('register', views.register, name='register'),
    path('registerCustomer', views.registerCustomer, name='registerCustomer'),
    path('customers', views.customers, name='customers'),

    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="password_reset.html"),name="reset_password"),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"),name="password_reset_complete"),
]