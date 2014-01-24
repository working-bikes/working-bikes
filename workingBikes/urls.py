from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'workingBikes.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^volunteer/', include('volunteer.urls', namespace='volunteer')),
	url(r'^$', RedirectView.as_view(url=reverse_lazy('volunteer:index'))),
)
