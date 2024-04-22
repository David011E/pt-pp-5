from django.urls import path
from .views import UserProfileView, CancelSubscriptionView

urlpatterns = [
    path('', UserProfileView.as_view(), name='userprofile'),
    path('cancel-subscription/<str:subscription_id>/', CancelSubscriptionView.as_view(), name='cancel_subscription'),
]
