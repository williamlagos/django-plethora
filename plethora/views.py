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

from .app import Images,Spreads,Uploads
from .content import Spreadables
# from .models import Product

from django.views import View
from django.http import JsonResponse

class ContentsView(View):
    def get(self, request):
        return JsonResponse({'contents': 'success'})

def start(request):
    e = Feedly()
    if request.method == 'GET':
        return e.start(request)

def media(request):
    u = Uploads()
    if request.method == 'GET':
        return u.media_chooser(request)

def spreaded(request):
    s = Spreadables()
    if request.method == 'GET':
        return s.view_spreaded(request)

def spreadspread(request):
    s = Spreadables()
    if request.method == 'GET':
        return s.spreadspread(request)
    elif request.method == 'POST':
        return s.spreadobject(request)

def spreadable(request):
    s = Spreadables()
    if request.method == 'GET':
        return s.view_spreadable(request)

def playable(request):
    s = Spreadables()
    if request.method == 'GET':
        return s.view_playable(request)

def imageview(request):
    s = Spreadables()
    if request.method == 'GET':
        return s.view_images(request)

def image(request):
    i = Images()
    if request.method == 'GET':
        return i.view_image(request)
    elif request.method == 'POST':
        return i.create_image(request)

def upload(request):
    u = Uploads()
    if request.method == 'GET':
        return u.view_content(request)
    elif request.method == 'POST':
        return u.upload_content(request)

def init_spread(request):
    spread = Spreads()
    if request.method == 'GET':
        return spread.start_spreadapp(request)

def main(request):
    graph = Spreads()
    if request.method == 'GET':
        return graph.view_spread(request)
    elif request.method == 'POST':
        return graph.create_spread(request)

def content(request):
    upload = Uploads()
    if request.method == 'GET':
        return upload.view_upload(request)