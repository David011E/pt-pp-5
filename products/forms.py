from django import forms
from .models import Product, Category
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from .widgets import CustomClearableFileInput

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        categories = Category.objects.all()
        category_choices = [(c.id, c.name) for c in categories]

        self.fields['category'].choices = category_choices
        self.fields['stripe_price_id'].label += ' | User must get this from stripe'  # Add suffix to the price label
        self.fields['price'].label += ' | (In cents)'  # Add suffix to the price label

        # Add CSS classes to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0 form-control'  # Apply form-control class to all fields

    # Define form layout using Crispy Forms
    helper = FormHelper()
    helper.form_method = 'post'
    helper.form_class = 'form mb-2'
    helper.label_class = 'control-label'
    helper.field_class = 'form-control'
    helper.layout = Layout(
        Field('category'),
        Field('name'),
        Field('description'),
        Field('stripe_price_id'),
        Field('price'),
        Field('image'),
    )

