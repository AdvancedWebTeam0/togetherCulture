from django import forms
from .models import EventTag, EventLabel


class EventSearchForm(forms.Form):
    tags = forms.ModelMultipleChoiceField(
        queryset=EventTag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    labels = forms.ModelMultipleChoiceField(
        queryset=EventLabel.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
