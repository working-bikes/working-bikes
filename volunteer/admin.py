import datetime

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.db import models
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

from volunteer.models import Volunteer, Timesheet, TimesheetApproval, VolunteerTask, Purchase
from volunteer.forms import TimesheetCreateForm

class VolunteerAdmin(admin.ModelAdmin):
	model = Volunteer

	list_display = ('name', 'type', 'is_member',)

	actions = ['add_event',]

	class AddEventForm(forms.Form):
		_selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
		day = forms.DateField()
		hours = forms.DecimalField(max_digits=4, decimal_places=2)
		notes = forms.CharField(widget=forms.Textarea)

	def add_event(self, request, queryset):
		form = None

		if 'apply' in request.POST:
			form = self.AddEventForm(request.POST)

			if form.is_valid():
				day = form.cleaned_data['day']
				hours = form.cleaned_data['hours']
				notes = form.cleaned_data['notes']

				count = 0
				for volunteer in queryset:
					timesheet = Timesheet.objects.create(day=day, volunteer=volunteer, hours=hours, notes=notes, from_event=True)
					timesheet.save()
					approval = TimesheetApproval.objects.create(timesheet=timesheet, approved_by=request.user)
					approval.save()
					count += 1

				self.message_user(request, 'Successfully added event for {count} volunteer(s).'.format(**locals()))
				return HttpResponseRedirect(request.get_full_path())

		if not form:
			form = self.AddEventForm(initial={'day': datetime.date.today, '_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

		return render_to_response('admin/add_event.html',
								  {
									'volunteers': queryset,
									'event_form': form,
								  },
								  context_instance=RequestContext(request))

	add_event.short_description = 'Add event for selected volunteers'

class TimesheetApprovalInline(admin.StackedInline):
	model = TimesheetApproval

class TimesheetAdmin(admin.ModelAdmin):
	model = Timesheet

	inlines = [
		TimesheetApprovalInline,
	]

	list_display = ('volunteer', 'day', 'hours', 'notes', 'from_event', 'approved',)
	list_filter = ('volunteer',)
	actions = ['approve',]

	def approve(self, request, queryset):
		for timesheet in queryset:
			try:
				approval = timesheet.timesheetapproval
			except TimesheetApproval.DoesNotExist:
				approval = TimesheetApproval.objects.create(timesheet=timesheet, approved_by=request.user)
				approval.save()
	approve.short_description = 'Approve selected timesheets'


class VolunteerTaskAdmin(admin.ModelAdmin):
	model = VolunteerTask
	list_display = ('title', 'description',)

class PurchaseAdmin(admin.ModelAdmin):
	model = Purchase
	list_display = ('description', 'volunteer', 'points',)
	list_filter = ('volunteer',)

admin.site.register(Volunteer, VolunteerAdmin)
admin.site.register(Timesheet, TimesheetAdmin)
admin.site.register(VolunteerTask, VolunteerTaskAdmin)
admin.site.register(Purchase, PurchaseAdmin)
