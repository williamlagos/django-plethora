from django.conf.urls import patterns,url,include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from efforia.pagseguro.urls import pagseguro_urlpatterns
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$','efforia.views.main'),
    (r'^efforia/',include('efforia.urls')),
#    (r'^promote/',include('promote.urls')),
    (r'^spread/',include('spread.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += pagseguro_urlpatterns()
