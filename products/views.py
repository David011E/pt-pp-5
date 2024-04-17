from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Product, Category
from django.conf import settings
from .models import Product
import sweetify

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

def all_services(request):
    products = Product.objects.all()

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)
            
        if 'category' in request.GET:
            categories = request.GET.getlist('category')
            products = products.filter(category__name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                sweetify.error(request, 'error!', text='You didnt enter any search criteria!', timer=5000)
                return redirect(reverse('all_services'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query) | Q(category__name__icontains=query)
            products = products.filter(queries)
    
    context = {
        "products": products,
        "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
    }
    return render(request, 'products/products.html', context)


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        product_id = self.kwargs["pk"]
        product = Product.objects.get(id=product_id)
        YOUR_DOMAIN = "http://127.0.0.1:8000"

        # Get the URL of the product image
        product_image_url = request.build_absolute_uri(product.image)

        checkout_session = stripe.checkout.Session.create(
            client_reference_id=request.user.id if request.user.is_authenticated else None,
            payment_method_types=['card'],
            mode='subscription',
            line_items=[
                {
                    'price': settings.STRIPE_PRICE_ID,  # Use price ID directly here
                    'quantity': 1,
                },
            ],
            metadata={
                "product_id": product.id
            },
            success_url=YOUR_DOMAIN + reverse('checkout_success'),  # Construct success URL using reverse
            cancel_url=YOUR_DOMAIN + reverse('checkout_cancel'),  # Construct cancel URL using reverse
            locale='en',
        )

        # Construct the checkout URL using the 'url' field from the session object
        checkout_url = checkout_session.url

        return redirect(checkout_url)

    

class checkout_success(TemplateView):
    template_name = "products/checkout_success.html"


class checkout_cancel(TemplateView):
    template = 'products/checkout_cancel.html'