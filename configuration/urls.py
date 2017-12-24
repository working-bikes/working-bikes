from django.contrib import admin
from django.conf import settings
from django.views.generic import RedirectView
from django.conf.urls import include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import reverse_lazy

admin.autodiscover()

urlpatterns = [
    url(settings.ADMIN_URL, admin.site.urls),
    url(r'^volunteer/', include('volunteer.urls')),
    url(r'^explorer/', include('explorer.urls')),
    url(r'^$', RedirectView.as_view(url=reverse_lazy('volunteer:index'))),
]

urlpatterns += staticfiles_urlpatterns()
