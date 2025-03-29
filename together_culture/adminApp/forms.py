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


class UserSearchForm(forms.Form):
    user = forms.CharField(label='user', 
                              max_length=50, 
                              help_text='User to search'
                              )
