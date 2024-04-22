from django.urls import path
from . import views

urlpatterns = [
    path('', views.results, name='results'),
    path('add/', views.add_review, name='add_review')
]
