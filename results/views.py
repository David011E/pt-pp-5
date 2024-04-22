from django.shortcuts import render

# Create your views here.
def results(request):
    """
    A view to return index page
    """
    return render(request, 'results/results.html')