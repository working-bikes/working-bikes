from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from volunteer import views

urlpatterns = patterns('',
		url(r'^add/$', views.VolunteerRegistrationView.as_view(), name='registration'),
		url(r'^profile/$', login_required(views.VolunteerProfileView.as_view()), name='profile'),
		url(r'^timesheets/$', login_required(views.TimesheetListView.as_view()), name='timesheets'),
		url(r'^timesheets/add/$', login_required(views.TimesheetCreateView.as_view()), name='timesheet_add'),
		url(r'^timesheets/delete/(?P<timesheet_id>[\d]+)/$', login_required(views.TimesheetDeleteView.as_view()), name='timesheet_delete'),
		url(r'^timesheets/(?P<timesheet_id>[\d]+)/$', login_required(views.TimesheetUpdateView.as_view()), name='timesheet'),
		url(r'^login/$', 'django.contrib.auth.views.login', { 'template_name': 'volunteer/login.html' }, name='login'), 
		url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
)
