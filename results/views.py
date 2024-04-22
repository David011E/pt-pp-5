from django.shortcuts import render
from .forms import ReviewForm

# Create your views here.
def results(request):
    """
    A view to return index page
    """
    return render(request, 'results/results.html')


def add_review(request):
    """ Add a review to the store """

    form = ReviewForm()
    template = 'results/add_review.html'
    context = {
        'form': form
    }

    return render(request, template, context)