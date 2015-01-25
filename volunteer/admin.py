import datetime

from django import forms
from django.contrib import admin
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from volunteer.models import Volunteer, Timesheet, TimesheetApproval, Task, Purchase, PurchaseApproval


class VolunteerAdmin(admin.ModelAdmin):
    model = Volunteer

    list_display = ('name', 'type', 'hours', 'points', 'is_member',)

    actions = ('add_event',)
    search_fields = ('name',)

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
                    timesheet = Timesheet.objects.create(day=day, volunteer=volunteer, hours=hours, notes=notes,
                                                         from_event=True)
                    timesheet.save()
                    approval = TimesheetApproval.objects.create(timesheet=timesheet, approved_by=request.user)
                    approval.save()
                    count += 1

                self.message_user(request, 'Successfully added event for {count} volunteer(s).'.format(**locals()))
                return HttpResponseRedirect(request.get_full_path())

        if not form:
            form = self.AddEventForm(initial={'day': datetime.date.today,
                                              '_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

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
    actions = ('approve',)

    def approve(self, request, queryset):
        for timesheet in queryset:
            try:
                approval = timesheet.timesheetapproval
            except TimesheetApproval.DoesNotExist:
                approval = TimesheetApproval.objects.create(timesheet=timesheet, approved_by=request.user)
                approval.save()

    approve.short_description = 'Approve selected timesheets'


class TaskAdmin(admin.ModelAdmin):
    model = Task
    list_display = ('title', 'description',)


class PurchaseApprovalInline(admin.StackedInline):
    model = PurchaseApproval


class PurchaseAdmin(admin.ModelAdmin):
    model = Purchase
    list_display = ('description', 'volunteer', 'points', 'approved',)
    list_filter = ('volunteer',)
    actions = ('approve',)

    inlines = [
        PurchaseApprovalInline,
    ]

    def approve(self, request, queryset):
        for purchase in queryset:
            try:
                approval = purchase.purchaseapproval
            except PurchaseApproval.DoesNotExist:
                approval = PurchaseApproval.objects.create(purchase=purchase, approved_by=request.user)
                approval.save()

    approve.short_description = 'Approve selected purchases'

admin.site.register(Volunteer, VolunteerAdmin)
admin.site.register(Timesheet, TimesheetAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Purchase, PurchaseAdmin)
