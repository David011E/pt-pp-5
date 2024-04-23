from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact, name='contact'),
    path('delete/<int:contact_id>/', views.delete_message, name='delete_message'),
]
