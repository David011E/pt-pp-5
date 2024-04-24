"""pt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from contact.views import (
    contact_admin,
    contact_details
)
from userprofile.views import UserProfileView
from products.views import (
    CreateCheckoutSessionView,
    checkout_success,
    checkout_cancel,
    StripeWebhookView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('home.urls')),
    path('products/', include('products.urls')),
    path('userprofile/', include('userprofile.urls')),
    path('results/', include('results.urls')),
    path('about/', include('about.urls')),
    path('contact/', include('contact.urls')),
    path('contact_admin/', contact_admin, name='contact_admin'),
    path('contact_details/<int:contact_id>/', contact_details, name='contact_details'),
    path('create-checkout-session/<pk>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('userprofile/', UserProfileView.as_view(), name='userprofile'),
    path('webhook/stripe/', StripeWebhookView.as_view(), name='stripe-webhook'),
    path('products/checkout_success/', checkout_success.as_view(), name='checkout_success'),  
    path('checkout_cancel/', checkout_cancel.as_view(), name='checkout_cancel'), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
