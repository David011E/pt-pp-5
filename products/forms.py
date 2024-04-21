from django import forms
from .models import Product, Category

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        categories = Category.objects.all()
        category_choices = [(c.id, c.name) for c in categories]

        self.fields['category'].choices = category_choices
        self.fields['price'].label += ' (In cents)'  # Add suffix to the price label

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
