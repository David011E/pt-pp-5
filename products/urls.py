from django.urls import path
from . import views
from .views import StripeWebhookView  # Import your view

urlpatterns = [
    path('', views.all_services, name='products'),  
    path('<int:product_id>/', views.product_details, name='product_details'),
    path('add/', views.add_product, name='add_product'), 
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),   
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),   
]
