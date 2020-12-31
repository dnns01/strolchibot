from django import forms
from .models import Timer, Klassenbuch, TextCommand


class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = ' w3-input '
            field.widget.attrs['placeholder'] = field.label
