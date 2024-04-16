from django.urls import path
from .views import CreateCheckoutSessionView
from . import views

urlpatterns = [
    path('', views.all_services, name='products'),
    path('create-checkout-session/<pk>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session')
]
