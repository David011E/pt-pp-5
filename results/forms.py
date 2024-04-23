from django import forms
from .models import Review
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        # Apply general styling to all fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control border-2 rounded'

        # Apply specific styling to the image field
        self.fields['image'].widget.attrs.update({
            'class': 'file-upload',  # Add a specific class for further styling with CSS
            'onchange': "readURL(this);",  # Optional JavaScript function to preview image
        })

        # Define form layout using Crispy Forms
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form mb-4'
        self.helper.label_class = 'control-label'
        self.helper.field_class = 'mb-3'
        self.helper.layout = Layout(
            Field('name'),
            Field('description'),
            'image',  # Use a string here if you don't need additional arguments
            FormActions(
                Submit('save', 'Update Review', css_class="btn btn-primary mt-4"),
                css_class='d-grid gap-2'  # Adjust this as needed for your layout
            )
        )
