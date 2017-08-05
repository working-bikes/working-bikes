from django.contrib import admin
from django.conf import settings
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy
from django.conf.urls import include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = [
    url(settings.ADMIN_URL, include(admin.site.urls)),
    url(r'^volunteer/', include('volunteer.urls', namespace='volunteer')),
    url(r'^explorer/', include('explorer.urls')),
    url(r'^$', RedirectView.as_view(url=reverse_lazy('volunteer:index'))),
]

urlpatterns += staticfiles_urlpatterns()
