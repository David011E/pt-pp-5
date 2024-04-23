from django.shortcuts import render

# Create your views here.
def contact_me(request):
    """
    A view to return index page
    """
    return render(request, 'contact/contact.html')