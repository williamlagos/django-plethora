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

from django.views import View
from django.http import JsonResponse

from .services import *

class ContentsView(View):
    
    def get(self, request):
        return JsonResponse({'contents': 'success'})

    def start(self, request):
        e = ContentService()
        if request.method == 'GET':
            return e.start(request)

    def media(self, request):
        u = ContentService()
        if request.method == 'GET':
            return u.media_chooser(request)

    def spreaded(self, request):
        s = ContentService()
        if request.method == 'GET':
            return s.view_spreaded(request)

    def spreadspread(self, request):
        s = ContentService()
        if request.method == 'GET':
            return s.spreadspread(request)
        elif request.method == 'POST':
            return s.spreadobject(request)

    def spreadable(self, request):
        s = ContentService()
        if request.method == 'GET':
            return s.view_spreadable(request)

    def playable(self, request):
        s = ContentService()
        if request.method == 'GET':
            return s.view_playable(request)

    def imageview(self, request):
        s = ContentService()
        if request.method == 'GET':
            return s.view_images(request)

    def image(self, request):
        i = ContentService()
        if request.method == 'GET':
            return i.view_image(request)
        elif request.method == 'POST':
            return i.create_image(request)

    def upload(self, request):
        u = ContentService()
        if request.method == 'GET':
            return u.view_content(request)
        elif request.method == 'POST':
            return u.upload_content(request)

    def init_spread(self, request):
        spread = ContentService()
        if request.method == 'GET':
            return spread.start_spreadapp(request)

    def main(self, request):
        graph = ContentService()
        if request.method == 'GET':
            return graph.view_spread(request)
        elif request.method == 'POST':
            return graph.create_spread(request)

    def content(self, request):
        upload = ContentService()
        if request.method == 'GET':
            return upload.view_upload(request)