from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_services, name='products'),  
    path('<int:product_id>/', views.product_details, name='product_details'),
]
