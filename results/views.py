from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import ReviewForm
from .models import Review 

import sweetify

# Create your views here.
def results(request):
    """
    A view to return index page with reviews
    """
    reviews = Review.objects.all()  # Fetch all reviews
    context = {
        'reviews': reviews,
    }
    return render(request, 'results/results.html', context)


def add_review(request):
    """ Add a review to the store """

    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            sweetify.success(request, 'Successfully added product!')
            return redirect(reverse('results'))
        else:
            sweetify.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ReviewForm()

    form = ReviewForm()
    template = 'results/add_review.html'
    context = {
        'form': form
    }

    return render(request, template, context)


def review_details(request, reviews_id):
    """
    A view to show individual service details
    """

    reveiws = get_object_or_404(Review, pk=reviews_id)  # Retrieve a single service object

    context = {
        'reveiws': reveiws,  # Pass the single service object to the template
    }

    return render(request, 'results/review_details.html', context)  