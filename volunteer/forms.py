import re

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from volunteer.models import Volunteer, Timesheet, Purchase, Task


class UserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')


class VolunteerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(VolunteerForm, self).__init__(*args, **kwargs)
        self.fields['preferred_tasks'].queryset = Task.objects.filter(active=True)

    acknowledged = forms.BooleanField()
    acknowledged.label = 'I Agree'

    class Meta:
        model = Volunteer
        exclude = ['user', ]

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']
        pattern = re.compile('^(1)?[\.\ -]?(\d{3})[\.\ -]?(\d{3})[\.\ -]?(\d{4})$')
        match = pattern.search(data)
        if not match:
            raise forms.ValidationError('Please enter a valid 10-digit phone number.')
        else:
            (country_code, area_code, exchange, subscriber) = match.groups()

        return '({0}) {1}-{2}'.format(area_code, exchange, subscriber)


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task


class HTML5Input(forms.widgets.Input):
    def __init__(self, type, attrs):
        self.input_type = type
        super(HTML5Input, self).__init__(attrs)


class TimesheetCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TimesheetCreateForm, self).__init__(*args, **kwargs)
        self.fields['task'].queryset = Task.objects.filter(active=True)

    class Meta:
        model = Timesheet
        exclude = ('volunteer', 'from_event',)
        widgets = {
            'hours': HTML5Input(type='number', attrs={'min': 0.25, 'step': 0.25})
        }


class PurchaseCreateForm(forms.ModelForm):
    class Meta:
        model = Purchase
        exclude = ('volunteer',)