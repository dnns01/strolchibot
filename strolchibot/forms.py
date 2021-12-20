from django import forms

from .models import Config, Command, Spotify, Counter


class BaseModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseModelForm, self).__init__(*args, **kwargs)
        add_classes(self.fields)


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        add_classes(self.fields)


def add_classes(fields):
    for field_name, field in fields.items():
        if type(field) is forms.fields.BooleanField:
            field.widget.attrs['class'] = ' w3-switch '
            field.label_suffix = ""
        elif type(field) is forms.models.ModelMultipleChoiceField:
            field.widget.attrs['class'] = ' w3-multiple-choice '
        else:
            field.widget.attrs['class'] = ' w3-input '
        field.widget.attrs['placeholder'] = field.label


class LinkProtectionConfigForm(BaseModelForm):
    class Meta:
        model = Config
        fields = ['link_protection_active', 'link_protection_permit_subs']


class CommandForm(BaseModelForm):
    class Meta:
        model = Command
        exclude = ['active']


class SpotifyForm(BaseModelForm):
    class Meta:
        model = Spotify
        fields = ['streamer']


class CounterForm(BaseModelForm):
    class Meta:
        model = Counter
        exclude = []
