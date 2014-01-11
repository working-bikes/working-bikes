from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from volunteer.models import Volunteer, Timesheet

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

class TimesheetCreateForm(forms.ModelForm):
	class Meta:
		model = Timesheet
		exclude = ['volunteer',]
