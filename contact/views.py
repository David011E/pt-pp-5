from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import ContactForm
from .models import Contact 

import sweetify

# Create your views here.
def contact(request):
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


def contact_admin(request):
    """ Where admin can view messages """

    contacts = Contact.objects.all()

    context = {
        'contact': contacts,
    }
    return render(request, 'contact/contact_admin.html', context)