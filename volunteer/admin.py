import datetime

from django import forms
from django.contrib import admin
from django.template import RequestContext
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from volunteer.models import Volunteer, Timesheet, TimesheetApproval, Task, Purchase, PurchaseApproval, PointsAward


class NiceUserModelAdmin(admin.ModelAdmin):
    """
    In addition to showing a user's username in related fields, show their full
    name too (if they have one and it differs from the username).
    """
    always_show_username = True

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(NiceUserModelAdmin, self).formfield_for_foreignkey(
                                                db_field, request, **kwargs)
        if db_field.rel.to == User:
            field.label_from_instance = self.get_user_label
        return field

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        field = super(NiceUserModelAdmin, self).formfield_for_manytomany(
                                                db_field, request, **kwargs)
        if db_field.rel.to == User:
            field.label_from_instance = self.get_user_label
        return field

    def get_user_label(self, user):
        name = user.get_full_name()
        username = user.username
        if not self.always_show_username:
            return name or username
        return (name and name != username and '%s (%s)' % (name, username)
                or username)


class VolunteerAdmin(admin.ModelAdmin):
    model = Volunteer

    list_display = ('name', 'type', 'hours', 'points', 'is_member',)

    actions = ('add_event',)
    search_fields = ('user__first_name', 'user__last_name')
    list_per_page = 25

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
            form = self.AddEventForm(initial={
                'day': datetime.date.today,
                '_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
            })

        return render_to_response(
            'admin/add_event.html',
            {
                'volunteers': queryset,
                'event_form': form,
            },
            context_instance=RequestContext(request)
        )

    add_event.short_description = 'Add event for selected volunteers'


class TimesheetApprovalInline(admin.StackedInline):
    model = TimesheetApproval


class TimesheetAdmin(admin.ModelAdmin):
    model = Timesheet

    inlines = [
        TimesheetApprovalInline,
    ]

    list_display = ('volunteer', 'day', 'hours', 'notes', 'from_event', 'approved',)
    actions = ('approve',)
    search_fields = ('volunteer__user__first_name', 'volunteer__user__last_name',)
    list_filter = ('day',)

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
    list_display = ('title', 'description', 'active')
    list_editable = ('active',)


class PurchaseApprovalInline(admin.StackedInline):
    model = PurchaseApproval


class PurchaseAdmin(admin.ModelAdmin):
    model = Purchase
    list_display = ('description', 'date', 'volunteer', 'points', 'approved',)
    actions = ('approve',)
    search_fields = ('volunteer__user__first_name', 'volunteer__user__last_name',)
    list_filter = ('date',)

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


class PointsAwardAdmin(NiceUserModelAdmin):
    model = PointsAward
    list_display = ('volunteer', 'points', 'reason', 'awarded_by', 'date')
    search_fields = ('volunteer__user__first_name', 'volunteer__user__last_name',)
    list_filter = ('date',)

admin.site.register(Volunteer, VolunteerAdmin)
admin.site.register(Timesheet, TimesheetAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(PointsAward, PointsAwardAdmin)
