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
	class Meta:
		model = Volunteer
		exclude = ['user',]
	
	def clean_phone_number(self):
		data = self.cleaned_data['phone_number']
		pattern = re.compile('^(1)?[\.\ -]?(\d{3})[\.\ -]?(\d{3})[\.\ -]?(\d{4})$')
		match = pattern.search(data)
		if not match:
			raise forms.ValidationError('Please enter a valid 10-digit phone number.')
		else:
			(countryCode, areaCode, exchange, subscriber) = match.groups()

		return '({0}) {1}-{2}'.format(areaCode, exchange, subscriber)

class TaskForm(forms.ModelForm):
	class Meta:
		model = Task

class TimesheetHoursInput(forms.Widget):
	def render(self, name, value, attrs=None):
		return '<input type="number" min="0.25" max="24" step="0.25" />'

class TimesheetCreateForm(forms.ModelForm):
	class Meta:
		model = Timesheet
		exclude = ['volunteer', 'from_event',]
		widgets = {
			'hours': TimesheetHoursInput(attrs={'min': 5, 'max': 10, 'step': 1})
		}

class PurchaseCreateForm(forms.ModelForm):
	class Meta:
		model = Purchase

	def clean_points(self):
		data = self.cleaned_data['points']
		volunteer = self.cleaned_data.get('volunteer', None)
		if volunteer is None:
			raise forms.ValidationError('Please select a volunteer.')
		volunteerID = volunteer.id
		volunteer = Volunteer.objects.get(pk=volunteerID)
		if volunteer is not None:
			if data > volunteer.points():
				raise forms.ValidationError('The volunteer has {0} points, which is not enough for this purchase ({1} points).'.format(volunteer.points(), data))
		return data
