from django import forms
from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView, DeleteView

from volunteer.models import Volunteer, Timesheet, Purchase
from volunteer.forms import UserForm, VolunteerForm, TimesheetCreateForm, PurchaseCreateForm


class VolunteerRegistrationView(TemplateView):
    template_name = 'volunteer/registration.html'

    def post(self, request):
        user_form = UserForm(request.POST, prefix='user')
        volunteer_form = VolunteerForm(request.POST, prefix='volunteer')

        if user_form.is_valid() and volunteer_form.is_valid():
            user = user_form.save()
            volunteer = volunteer_form.save(commit=False)
            volunteer.user = user
            volunteer.save()

            volunteer = authenticate(username=user_form.cleaned_data['username'],
                                     password=user_form.cleaned_data['password1'])
            if volunteer is not None:
                login(request, volunteer)
                return HttpResponseRedirect(reverse('volunteer:profile'))

            else:
                return HttpResponseRedirect(reverse('volunteer:login'))

        else:
            return render(request, self.template_name, {'userform': user_form, 'volunteerform': volunteer_form})

    def get_context_data(self, **kwargs):
        context = super(VolunteerRegistrationView, self).get_context_data(**kwargs)
        context['userform'] = UserForm(prefix='user')
        context['volunteerform'] = VolunteerForm(prefix='volunteer')
        return context


class VolunteerProfileView(DetailView):
    template_name = 'volunteer/profile.html'

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Volunteer, user=self.request.user)


class PurchaseListView(ListView):
    template_name = 'volunteer/purchase_list.html'

    def get_queryset(self):
        return Purchase.objects.filter(volunteer=Volunteer.objects.get(user=self.request.user)).order_by('-date')


class PurchaseCreateView(CreateView):
    form_class = PurchaseCreateForm
    template_name = 'volunteer/purchase_form.html'

    def get_success_url(self):
        return reverse('volunteer:purchases')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.volunteer = Volunteer.objects.get(user=self.request.user)
        points = form.cleaned_data['points']
        if points > obj.volunteer.points():
            raise forms.ValidationError(
                'The volunteer has {0} points, which is not enough for this purchase ({1} points).'.format(
                    obj.volunteer.points(), points))
        obj.save()
        return HttpResponseRedirect(self.get_success_url())


class PurchaseUpdateView(UpdateView):
    form_class = PurchaseCreateForm
    template_name = 'volunteer/purchase_form.html'

    def get_success_url(self):
        return reverse('volunteer:purchases')

    def get_object(self, *args, **kwargs):
        try:
            purchase = Purchase.objects.get(pk=self.kwargs['purchase_id'])
            if purchase.approved():
                raise Http404
            return purchase
        except Purchase.DoesNotExist:
            raise Http404


class PurchaseDeleteView(DeleteView):
    model = Timesheet

    def get_success_url(self):
        return reverse('volunteer:purchases')

    def get_object(self, *args, **kwargs):
        try:
            purchase = Purchase.objects.get(pk=self.kwargs['purchase_id'])
            if purchase.approved():
                raise Http404
            return purchase
        except Purchase.DoesNotExist:
            raise Http404


class TimesheetListView(ListView):
    template_name = 'volunteer/timesheet_list.html'

    def get_queryset(self):
        return Timesheet.objects.filter(volunteer=Volunteer.objects.get(user=self.request.user)).order_by('-day')


class TimesheetDetailView(DetailView):
    template_name = 'volunteer/timesheet_detail.html'
    object_name = 'timesheet'

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Timesheet, volunteer=Volunteer.objects.get(user=self.request.user),
                                 pk=self.kwargs['timesheet_id'])


class TimesheetCreateView(CreateView):
    form_class = TimesheetCreateForm
    template_name = 'volunteer/timesheet_form.html'

    def form_valid(self, form):
        obj = None
        try:
            obj = form.save(commit=False)
            obj.volunteer = Volunteer.objects.get(user=self.request.user)
            existing_timesheet = Timesheet.objects.get(volunteer=Volunteer.objects.get(user=self.request.user),
                                                       day=obj.day, from_event=False)
            if existing_timesheet.from_event:
                obj.save()
                return HttpResponseRedirect(reverse('volunteer:timesheets'))
            else:
                return render(self.request, self.template_name,
                              {'form': form, 'timesheet_exists': True, 'existing_timesheet': existing_timesheet})
        except Timesheet.DoesNotExist:
            obj.save()
            return HttpResponseRedirect(reverse('volunteer:timesheets'))


class TimesheetUpdateView(UpdateView):
    form_class = TimesheetCreateForm
    template_name = 'volunteer/timesheet_form.html'

    def get_success_url(self):
        return reverse('volunteer:timesheet', args=(self.kwargs['timesheet_id'],))

    def get_object(self, *args, **kwargs):
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

    def get_object(self, *args, **kwargs):
        try:
            timesheet = Timesheet.objects.get(pk=self.kwargs['timesheet_id'])
            if timesheet.approved():
                raise Http404
            return timesheet
        except Timesheet.DoesNotExist:
            raise Http404
