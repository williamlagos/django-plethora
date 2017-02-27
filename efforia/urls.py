from django.conf.urls import url,include
from efforia.views import *

urlpatterns = [
    url(r'^mosaic', mosaic),
    url(r'^config', config),
    url(r'^profile', profile),
    url(r'^basket', basket),
    url(r'^photo', photo),
    url(r'^appearance', appearance),
    url(r'^options', options),
    url(r'^place', place),
    url(r'^password', password),
    url(r'^integrations', integrations),
    url(r'^enter', authenticate),
    url(r'^leave', leave),
    url(r'^delete', delete),
    url(r'^userid', ids),
    url(r'^search', search),
    url(r'^explore', search),
    url(r'^known', explore),
    url(r'^activity', activity),
    url(r'^following', following),
    url(r'^follow', follow),
    url(r'^unfollow', unfollow),
    url(r'^twitter/post', twitter_post),
    url(r'^facebook/post', facebook_post),
    url(r'^facebook/eventcover', facebook_eventcover),
    url(r'^facebook/event', facebook_event),
    url(r'^participate', participate),
    url(r'^tutorial', tutorial),
    url(r'^pagseguro/cart', pagsegurocart),
    url(r'^pagseguro', pagseguro),
    url(r'^paypal/cart', paypalcart),
    url(r'^paypal', paypal),
    url(r'^pages', page),
    url(r'^pageview', pageview),
    url(r'^pageedit', pageedit),
    url(r'^discharge', discharge),
    url(r'^recharge', recharge),
    url(r'^balance', balance),
    url(r'^deadlines', deadlines),
]

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
admin.autodiscover()

urlpatterns += [
    url(r'^$', main),
    url(r'^efforia/',include('efforia.urls')),
    url(r'^spread/',include('spread.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

]

urlpatterns += staticfiles_urlpatterns()
