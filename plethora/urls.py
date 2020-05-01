from django.conf.urls import url,include
from .views import *

urlpatterns = [
    url(r'^$', init_spread),
    url(r'^spreadable', spreadable),
    url(r'^spreaded', spreaded),
    url(r'^spreadspread', spreadspread),
    url(r'^spread', main),
    url(r'^playable', playable),
    url(r'^images', image),
    url(r'^image', imageview),
    url(r'^contents', content),
    url(r'^expose', upload),
    url(r'^media', media),
]