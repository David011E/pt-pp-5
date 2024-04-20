from django.urls import path
from . import views
from .views import CancelSubscriptionView

urlpatterns = [
    path('', views.UserProfileView.as_view(), name='userprofile'),
    path('cancel-subscription/<str:subscription_id>/', views.CancelSubscriptionView.as_view(), name='cancel_subscription'),
]
