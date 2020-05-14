#!/usr/bin/python
#
# This file is part of django-plethora project.
#
# Copyright (C) 2011-2020 William Oliveira de Lagos <william.lagos@icloud.com>
#
# Plethora is free software: you can redistribute it and/or modify
# it under the terms of the Lesser GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Plethora is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Plethora. If not, see <http://www.gnu.org/licenses/>.
#

from django.conf.urls import url,include
from django.urls import path

from .views import *

urlpatterns = [
    path('', ContentsView.as_view()),
    # url(r'^$', init_spread),
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