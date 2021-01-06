from django import forms
from .models import Config


class BaseModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseModelForm, self).__init__(*args, **kwargs)
        add_classes(self.fields)


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        add_classes(self.fields)


class LinkProtectionConfigForm(BaseForm):
    active = forms.BooleanField(required=False)
    permit_subs = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(LinkProtectionConfigForm, self).__init__(*args, **kwargs)
        self.fields["active"].initial = Config.objects.get(key="LinkProtectionActive").value == "1"
        self.fields["permit_subs"].initial = Config.objects.get(key="LinkProtectionPermitSubs").value == "1"
        pass

    def save(self):
        active = Config.objects.get(key="LinkProtectionActive")
        active.value = "1" if self.cleaned_data["active"] else "0"
        active.save()

        permit_subs = Config.objects.get(key="LinkProtectionPermitSubs")
        permit_subs.value = "1" if self.cleaned_data["permit_subs"] else "0"
        permit_subs.save()


def add_classes(fields):
    for field_name, field in fields.items():
        if type(field) is forms.fields.BooleanField:
            field.widget.attrs['class'] = ' w3-switch '
            field.label_suffix = ""
        else:
            field.widget.attrs['class'] = ' w3-input '
        field.widget.attrs['placeholder'] = field.label
