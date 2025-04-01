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


class MemberTypeFilterForm(forms.Form):
    CHOICES = [
        ('Community Membership', 'Community Membership'),
        ('Workspace Membership: Touchdown', 'Workspace Membership: Touchdown'),
        ('Workspace Membership: Dedicated', 'Workspace Membership: Dedicated'),
    ]
    
    member_type = forms.ChoiceField(choices=CHOICES, required=True)


class UserTypeFilterForm(forms.Form):
    #first value is the actual value that gets submitted while the second one is visible in UI.
    CHOICES = [
        ('NORMAL_USER', 'Non member'),
        ('MEMBER', 'Member'),
    ]
    
    user_type = forms.ChoiceField(choices=CHOICES, required=True)
