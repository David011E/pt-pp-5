from django.urls import path
from . import views

urlpatterns = [
    path('', views.results, name='results'),
    path('add/', views.add_review, name='add_review'),
    path('<int:reviews_id>/', views.review_details, name='review_details'),
    path('edit/<int:reviews_id>/', views.edit_review, name='edit_review'), 
    path('delete/<int:reviews_id>/', views.delete_review, name='delete_review'),   
]
