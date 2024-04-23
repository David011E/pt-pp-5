from django.shortcuts import render, redirect, reverse
from .forms import ContactForm
from .models import Contact 

import sweetify

# Create your views here.
def contact_me(request):
    """ Contact me form """
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            sweetify.success(request, 'Your message was successfully sent!')
            return redirect(reverse('contact'))
        else:
            sweetify.error(request, 'Failed to a message.')
    else:
        form = ContactForm()

    form = ContactForm()
    template = 'contact/contact.html'
    context = {
        'form': form
    }
    return render(request, template, context)