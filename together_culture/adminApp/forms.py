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
    members = forms.CharField(label='members', max_length=50, help_text='Member name to search')

    def clean_members(self):
        return self.cleaned_data['members']

