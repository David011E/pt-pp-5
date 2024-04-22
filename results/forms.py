from django import forms
from .models import Review
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'

    

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        # Add CSS classes to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0 form-control'  # Apply form-control class to all fields

        # Define form layout using Crispy Forms
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form mb-2'
        self.helper.label_class = 'control-label'
        self.helper.field_class = 'form-control'
        self.helper.layout = Layout(
            Field('name'),
            Field('description'),
            Field('image'),
        )
