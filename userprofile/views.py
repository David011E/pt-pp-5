from django.shortcuts import render

# Create your views here.
def userprofile(request):
    """
    A view to return index page
    """
    return render(request, 'userprofile/userprofile.html')