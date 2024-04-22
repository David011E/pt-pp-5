from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
from django.db.models import Q
from django.contrib import messages
from django.db.models.functions import Lower
from .models import Product, Category
from allauth.account.models import EmailAddress
from django.conf import settings
from .models import Product
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProductForm

import stripe
import sweetify

stripe.api_key = settings.STRIPE_SECRET_KEY

def all_services(request):
    products = Product.objects.all()

    query = None
    categories = None
    sort = None
    direction = None

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
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('all_services'))

            
            queries = Q(name__icontains=query) | Q(description__icontains=query) | Q(category__name__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'
    
    context = {
        "products": products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }
    return render(request, 'products/products.html', context)


class CreateCheckoutSessionView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        product_id = self.kwargs["pk"]
        product = Product.objects.get(id=product_id)
        YOUR_DOMAIN = "http://127.0.0.1:8000"

        # Get the URL of the product image
        product_image_url = request.build_absolute_uri(product.image)

        # Retrieve the user's email address
        email_address = get_object_or_404(EmailAddress, user=request.user, primary=True)
        
        # Retrieve or create a Stripe Customer object for the user if authenticated
        if request.user.is_authenticated:
            try:
                customer = stripe.Customer.retrieve(email_address.stripe_customer_id)
            except stripe.error.InvalidRequestError:
                # If the customer doesn't exist, create a new one
                customer = stripe.Customer.create(email=email_address.email)
                email_address.stripe_customer_id = customer.id
                email_address.save()
        else:
            customer = None

        # Check if the user is already subscribed to the product using Stripe API
        if customer:
            subscriptions = stripe.Subscription.list(customer=customer.id)
            for subscription in subscriptions.auto_paging_iter():
                if subscription['status'] == 'active' and subscription['items']['data'][0]['price']['id'] == product.stripe_price_id:
                    messages.error(request, "You are already subscribed to this product.")
                    return redirect(reverse('checkout_cancel'))

        # Continue with creating the checkout session
        checkout_session = stripe.checkout.Session.create(
            client_reference_id=request.user.id if request.user.is_authenticated else None,
            payment_method_types=['card'],
            mode='subscription',
            customer=customer.id if customer else None,  # Use existing customer if authenticated
            line_items=[
                {
                    'price': product.stripe_price_id,  # Use price ID directly here
                    'quantity': 1,
                },
            ],
            metadata={
                "product_id": product.id
            },
            success_url=YOUR_DOMAIN + reverse('userprofile'),  # Construct success URL using reverse
            cancel_url=YOUR_DOMAIN + reverse('checkout_cancel'),  # Construct cancel URL using reverse
            locale='en',
        )

        # Construct the checkout URL using the 'url' field from the session object
        checkout_url = checkout_session.url

        return redirect(checkout_url)
    

def product_details(request, product_id):
    """
    A view to show individual service details
    """

    product = get_object_or_404(Product, pk=product_id)  # Retrieve a single service object

    context = {
        'product': product,  # Pass the single service object to the template
    }

    return render(request, 'products/product_details.html', context)  

    

class checkout_success(TemplateView):
    template_name = "products/checkout_success.html"


class checkout_cancel(TemplateView):
    template_name = 'products/checkout_cancel.html'


class StripeWebhookView(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(StripeWebhookView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET  # Replace 'whsec_...' with your actual webhook signing secret

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError:
            # Invalid payload
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError:
            # Invalid signature
            return HttpResponse(status=400)

        # Handle the event
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            # Handle the checkout session completion
            handle_checkout_session(session)

        # Respond to Stripe that the webhook was received
        return JsonResponse({'status': 'success'})

def handle_checkout_session(session):
    # Implement your business logic here
    print("Checkout session completed with session ID:", session['id'])


@login_required
def add_product(request):
    """ Add a product to the store """

    if not request.user.is_superuser:
        sweetify.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            sweetify.success(request, 'Successfully added product!')
            return redirect(reverse('product_details', args=[product.id]))
        else:
            sweetify.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
        
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)

@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """

    if not request.user.is_superuser:
        sweetify.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            sweetify.success(request, 'Successfully updated product!')
            return redirect(reverse('product_details', args=[product.id]))
        else:
            sweetify.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        sweetify.info(request, f'You are editing {product.name}')


    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)

@login_required
def delete_product(request, product_id):
    """ Delete a product in the store """

    if not request.user.is_superuser:
        sweetify.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    sweetify.success(request, 'Product deleted!')
    return redirect(reverse('products'))