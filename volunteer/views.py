import time
from datetime import date

from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.db.models import Q
from django.db.models import Sum
from django.http import Http404

from volunteer.models import Volunteer, Timesheet, Purchase
from volunteer.forms import UserForm, VolunteerForm, TimesheetCreateForm, PurchaseCreateForm

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

class PurchaseListView(ListView):
	template_name = 'volunteer/purchase_list.html'

	def get_queryset(self):
		return Purchase.objects.filter(volunteer=Volunteer.objects.get(user=self.request.user)).order_by('-date')

class PurchaseCreateView(CreateView):
	form_class = PurchaseCreateForm
	template_name = 'volunteer/purchase_form.html'

	def dispatch(self, request, *args, **kwargs):
		if not self.request.user.has_perm('volunteer.add_purchase'):
			raise Http404
		return super(PurchaseCreateView, self).dispatch(request, *args, **kwargs)

	def get_success_url(self):
		return reverse('volunteer:purchases')

class PurchaseUpdateView(UpdateView):
	form_class = PurchaseCreateForm
	template_name = 'volunteer/purchase_form.html'

	def dispatch(self, request, *args, **kwargs):
		if not self.request.user.has_perm('volunteer.update_purchase'):
			raise Http404
		return super(PurchaseUpdateView, self).dispatch(request, *args, **kwargs)

	def get_success_url(self):
		return reverse('volunteer:purchases')

	def get_object(self):
		return get_object_or_404(Purchase, pk=self.kwargs['purchase_id'])

class PurchaseDeleteView(DeleteView):
	model = Timesheet

	def dispatch(self, request, *args, **kwargs):
		if not self.request.user.has_perm('volunteer.delete_purchase'):
			raise Http404
		return super(PurchaseDeleteView, self).dispatch(request, *args, **kwargs)

	def get_success_url(self):
		return reverse('volunteer:purchases')

	def get_object(self):
		return get_object_or_404(Purchase, pk=self.kwargs['purchase_id'])

class TimesheetListView(ListView):
	template_name = 'volunteer/timesheet_list.html'

	def get_queryset(self):
		return Timesheet.objects.filter(volunteer=Volunteer.objects.get(user=self.request.user)).order_by('-day')

class TimesheetDetailView(DetailView):
	template_name = 'volunteer/timesheet_detail.html'
	object_name = 'timesheet'

	def get_object(self):
		return get_object_or_404(Timesheet, volunteer=Volunteer.objects.get(user=self.request.user), pk=self.kwargs['timesheet_id'])

class TimesheetCreateView(CreateView):
	form_class = TimesheetCreateForm
	template_name = 'volunteer/timesheet_form.html'

	def form_valid(self, form):
		try:
			obj = form.save(commit=False)
			obj.volunteer = Volunteer.objects.get(user=self.request.user)
			existingTimesheet = Timesheet.objects.get(volunteer=Volunteer.objects.get(user=self.request.user), day=obj.day, from_event=False)
			if existingTimesheet.from_event:
				obj.save()
				return HttpResponseRedirect(reverse('volunteer:timesheets'))
			else:
				return render(self.request, self.template_name, {'form': form, 'timesheet_exists': True, 'existingTimesheet': existingTimesheet})
		except Timesheet.DoesNotExist:
			obj.save()
			return HttpResponseRedirect(reverse('volunteer:timesheets'))

class TimesheetUpdateView(UpdateView):
	form_class = TimesheetCreateForm
	template_name = 'volunteer/timesheet_form.html'

	def get_success_url(self):
		return reverse('volunteer:timesheet', args=(self.kwargs['timesheet_id'],))

	def get_object(self):
		try:
			timesheet = Timesheet.objects.get(pk=self.kwargs['timesheet_id'])
			if timesheet.approved():
				raise Http404
			return timesheet
		except Timesheet.DoesNotExist:
			raise Http404

class TimesheetDeleteView(DeleteView):
	model = Timesheet

	def get_success_url(self):
		return reverse('volunteer:timesheets')

	def get_object(self):
		try:
			timesheet = Timesheet.objects.get(pk=self.kwargs['timesheet_id'])
			if timesheet.approved():
				raise Http404
			return timesheet
		except Timesheet.DoesNotExist:
			raise Http404
