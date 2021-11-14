from django import forms


class ClipSearchForm(forms.Form):
    search = forms.CharField(label="Search", required=False)

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        add_classes(self.fields)


def add_classes(fields):
    for field_name, field in fields.items():
        if type(field) is forms.fields.BooleanField:
            field.widget.attrs['class'] = ' w3-switch '
            field.label_suffix = ""
        else:
            field.widget.attrs['class'] = ' w3-input'
        field.widget.attrs['placeholder'] = field.label
