from django.conf.urls import url
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.views import login, logout
from django.contrib.auth.decorators import login_required

from volunteer import views

urlpatterns = [
    url(r'^$', RedirectView.as_view(url=reverse_lazy('volunteer:profile')), name='index'),
    url(r'^add/$', views.VolunteerRegistrationView.as_view(), name='registration'),
    url(r'^profile/$', login_required(views.VolunteerProfileView.as_view()), name='profile'),
    url(r'^purchases/$', login_required(views.PurchaseListView.as_view()), name='purchases'),
    url(r'^purchases/add/$', login_required(views.PurchaseCreateView.as_view()), name='purchase_add'),
    url(r'^purchases/delete/(?P<purchase_id>[\d]+)/$', login_required(views.PurchaseDeleteView.as_view()), name='purchase_delete'),
    url(r'^purchases/(?P<purchase_id>[\d]+)/$', login_required(views.PurchaseUpdateView.as_view()), name='purchase'),
    url(r'^timesheets/$', login_required(views.TimesheetListView.as_view()), name='timesheets'),
    url(r'^timesheets/add/$', login_required(views.TimesheetCreateView.as_view()), name='timesheet_add'),
    url(r'^timesheets/delete/(?P<timesheet_id>[\d]+)/$', login_required(views.TimesheetDeleteView.as_view()), name='timesheet_delete'),
    url(r'^timesheets/(?P<timesheet_id>[\d]+)/$', login_required(views.TimesheetDetailView.as_view()), name='timesheet'),
    url(r'^timesheets/update/(?P<timesheet_id>[\d]+)/$', login_required(views.TimesheetUpdateView.as_view()), name='timesheet_update'),
    url(r'^login/$', login, {'template_name': 'volunteer/login.html'}, name='login'),
    url(r'^logout/$', logout, name='logout'),
]
