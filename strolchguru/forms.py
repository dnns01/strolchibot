from django import forms

from strolchibot.forms import add_classes, BaseModelForm
from .models import Clip


class ClipSearchForm(forms.Form):
    search = forms.CharField(label="Search", required=False)

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        add_classes(self.fields)


class ClipEditForm(BaseModelForm):
    class Meta:
        model = Clip
        fields = ['custom_title', 'tags']
        widgets = {'tags': forms.widgets.CheckboxSelectMultiple()}
