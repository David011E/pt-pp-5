from django import forms
from .models import Contact
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)

        # Apply general styling to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control border-2 rounded'

        # Define form layout using Crispy Forms
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form mb-4'
        self.helper.label_class = 'control-label'
        self.helper.field_class = 'mb-3'
        self.helper.layout = Layout(
            Field('name'),
            Field('email'),
            Field('description'),
            FormActions(
                Submit('submit', 'Submit', css_class="btn btn-primary mt-4"),
                css_class='d-grid gap-2'  # Adjust this as needed for your layout
            )
        )
