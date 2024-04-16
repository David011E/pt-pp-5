from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_services, name='products'),
    path('checkout_success/', views.checkout_success, name='products'),
    path('checkout_cancel/', views.checkout_cancel, name='products'),
]
