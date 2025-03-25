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


class MemberSearchForm(forms.Form):
    member = forms.CharField(label='member', 
                              max_length=50, 
                              help_text='Member to search'
                              )
