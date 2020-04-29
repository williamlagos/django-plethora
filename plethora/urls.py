from django.conf.urls import url,include
from plethora.views import *

urlpatterns = [
    url(r'^spread$', init_spread),
    url(r'^spread/products', store_main),
    url(r'^spread/cancel', cancel),
    url(r'^spread/delivery', delivery),
    url(r'^spread/correios', mail),
    url(r'^spread/spreadable', spreadable),
    url(r'^spread/spreaded', spreaded),
    url(r'^spread/spreadspread', spreadspread),
    url(r'^spread/spread', main),
    url(r'^spread/playable', playable),
    url(r'^spread/images', image),
    url(r'^spread/image', imageview),
    url(r'^spread/contents', content),
    url(r'^spread/expose', upload),
    url(r'^spread/media', media),
    url(r'^spread/productimage', product_image)
]

# from efforia.views import *
#
# urlpatterns += [
#     url(r'^efforia/mosaic', mosaic),
#     url(r'^efforia/config', config),
#     url(r'^efforia/profile', profile),
#     url(r'^efforia/basket', basket),
#     url(r'^efforia/photo', photo),
#     url(r'^efforia/appearance', appearance),
#     url(r'^efforia/options', options),
#     url(r'^efforia/place', place),
#     url(r'^efforia/password', password),
#     url(r'^efforia/integrations', integrations),
#     url(r'^efforia/enter', authenticate),
#     url(r'^efforia/leave', leave),
#     url(r'^efforia/delete', delete),
#     url(r'^efforia/userid', ids),
#     url(r'^efforia/search', search),
#     url(r'^efforia/explore', search),
#     url(r'^efforia/known', explore),
#     url(r'^efforia/activity', activity),
#     url(r'^efforia/following', following),
#     url(r'^efforia/follow', follow),
#     url(r'^efforia/unfollow', unfollow),
#     url(r'^efforia/twitter/post', twitter_post),
#     url(r'^efforia/facebook/post', facebook_post),
#     url(r'^efforia/facebook/eventcover', facebook_eventcover),
#     url(r'^efforia/facebook/event', facebook_event),
#     url(r'^efforia/participate', participate),
#     url(r'^efforia/tutorial', tutorial),
#     url(r'^efforia/pagseguro/cart', pagsegurocart),
#     url(r'^efforia/pagseguro', pagseguro),
#     url(r'^efforia/paypal/cart', paypalcart),
#     url(r'^efforia/paypal', paypal),
#     url(r'^efforia/pages', page),
#     url(r'^efforia/pageview', pageview),
#     url(r'^efforia/pageedit', pageedit),
#     url(r'^efforia/discharge', discharge),
#     url(r'^efforia/recharge', recharge),
#     url(r'^efforia/balance', balance),
#     url(r'^efforia/deadlines', deadlines),
# ]

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django_distill import distill_url

admin.autodiscover()

def getNone(): return None

urlpatterns += [
    distill_url(r'^$', start, name='home', distill_func=getNone),
    url(r'^socialize/',include('socialize.urls')),
    url(r'^shipping/',include('shipping.urls')),
    url(r'^feedly/',include('feedly.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
]

urlpatterns += staticfiles_urlpatterns()
