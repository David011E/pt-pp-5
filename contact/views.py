from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import ContactForm
from .models import Contact 
from django.contrib.auth.decorators import login_required

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


@login_required
def contact_admin(request):
    """ Where admin can view messages """

    contacts = Contact.objects.all()

    template = 'contact/contact_admin.html'

    context = {
        'contact': contacts,
    }
    return render(request, template, context)


@login_required
def contact_details(request, contact_id):
    """
    A view to show individual contact details
    """

    # Retrieve a single contact object based on contact_id
    message = get_object_or_404(Contact, pk=contact_id)

    template = 'contact/contact_details.html'

    context = {
        'message': message,  # Pass the single contact object to the template
    }

    return render(request, template, context)


@login_required
def delete_message(request, contact_id):
    """ Delete a message in the store """

    if not request.user.is_superuser:
        sweetify.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    
    message = get_object_or_404(Contact, pk=contact_id)
    message.delete()
    sweetify.success(request, 'Message deleted!')
    return redirect(reverse('contact'))