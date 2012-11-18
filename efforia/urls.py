from django.conf.urls import patterns,url,include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$','core.views.main'),
    (r'^enter','core.views.authenticate'),
    (r'^leave','core.views.leave'),
    (r'^verify','core.views.verify_login'),
    (r'^discharge','store.views.discharge'),
    (r'^recharge','store.views.recharge'),
    (r'^balance','store.views.balance'),
    (r'^accounts/', include('userena.urls')),
    # Examples:
    # url(r'^$', 'efforia.views.home', name='home'),
    # url(r'^efforia/', include('efforia.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += staticfiles_urlpatterns()
