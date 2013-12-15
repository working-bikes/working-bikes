from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from volunteer.models import Volunteer, Timesheet, TimesheetApproval

admin.site.unregister(User)

class VolunteerInline(admin.StackedInline):
	model = Volunteer

class VolunteerAdmin(UserAdmin):
	inlines = [
		VolunteerInline,
	]

class TimesheetApprovalInline(admin.StackedInline):
	model = TimesheetApproval

class TimesheetAdmin(admin.ModelAdmin):
	model = Timesheet

	inlines = [
		TimesheetApprovalInline,
	]

	list_display = ('user', 'day', 'approved',)
	list_filter = ('user',)

admin.site.register(User, VolunteerAdmin)
admin.site.register(Timesheet, TimesheetAdmin)
