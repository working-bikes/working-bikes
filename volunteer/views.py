from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.db.models import Q

from volunteer.models import Volunteer, Timesheet
from volunteer.forms import UserForm, VolunteerForm, TimesheetCreateForm

class VolunteerRegistrationView(TemplateView):
	template_name = 'volunteer/registration.html'

	def post(self, request):
		userForm = UserForm(request.POST, prefix='user')
		volunteerForm = VolunteerForm(request.POST, prefix='volunteer')

		if userForm.is_valid() and volunteerForm.is_valid():
			user = userForm.save()
			volunteer = volunteerForm.save(commit=False)
			volunteer.user = user
			volunteer.save()

			volunteer = authenticate(username=userForm.cleaned_data['username'], password=userForm.cleaned_data['password1'])
			if volunteer is not None:
				login(request, volunteer)
				return HttpResponseRedirect(reverse('volunteer:profile'))

			else:
				return HttpResponseRedirect(reverse('volunteer:login'))

		else:
			return render(request, self.template_name, {'userform': userForm, 'volunteerform': volunteerForm })

	def get_context_data(self, **kwargs):
		context = super(VolunteerRegistrationView, self).get_context_data(**kwargs)
		context['userform'] = UserForm(prefix='user')
		context['volunteerform'] = VolunteerForm(prefix='volunteer')
		return context

class VolunteerProfileView(DetailView):
	template_name = 'volunteer/profile.html'

	def get_object(self):
		return get_object_or_404(Volunteer, user=self.request.user)

class TimesheetListView(ListView):
	template_name = 'volunteer/timesheet_list.html'

	def get_queryset(self):
		return Timesheet.objects.filter(user=self.request.user).order_by('-day')

class TimesheetCreateView(CreateView):
	form_class = TimesheetCreateForm
	template_name = 'volunteer/timesheet_form.html'

	def form_valid(self, form):
		try:
			obj = form.save(commit=False)
			obj.user = self.request.user
			obj.save()
			return HttpResponseRedirect(reverse('volunteer:timesheets'))
		except IntegrityError:
			return render(self.request, self.template_name, {'form': form, 'timesheet_exists': True})

class TimesheetUpdateView(UpdateView):
	form_class = TimesheetCreateForm
	template_name = 'volunteer/timesheet_form.html'

	def get_success_url(self):
		return reverse('volunteer:timesheets')

	def get_object(self):
		return get_object_or_404(Timesheet, pk=self.kwargs['timesheet_id'], user=self.request.user)

class TimesheetDeleteView(DeleteView):
	model = Timesheet

	def get_success_url(self):
		return reverse('volunteer:timesheets')

	def get_object(self):
		return get_object_or_404(Timesheet, pk=self.kwargs['timesheet_id'], user=self.request.user)
