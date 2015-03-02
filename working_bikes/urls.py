from django.contrib import admin
from django.conf import settings
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(settings.ADMIN_URL, include(admin.site.urls)),
    url(r'^volunteer/', include('volunteer.urls', namespace='volunteer')),
    url(r'^$', RedirectView.as_view(url=reverse_lazy('volunteer:index'))),
)

urlpatterns += staticfiles_urlpatterns()
