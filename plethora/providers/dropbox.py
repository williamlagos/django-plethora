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

from unicodedata import normalize
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse as response
from django.http import HttpResponseRedirect as redirect
from django.conf import settings


class DropboxExternalProvider:

    def __init__(self):
        pass

    def view_image(self, request):
        return render(request, 'image.pug', {'static_url': settings.STATIC_URL}, content_type='text/html')

    def upload_image(self, request):
        photo = request.FILES['Filedata'].read()
        dropbox = Dropbox()
        link = dropbox.upload_and_share(photo)
        res = self.url_request(link)
        url = '%s?dl=1' % res
        return url

    def create_image(self, request):
        u = self.current_user(request)
        if 'description' in request.POST:
            image = list(Image.objects.filter(user=u))[-1:][0]
            descr = request.POST['description']
            image.description = descr
            image.save()
            return response('Description added to image successfully')
        i = Image(link=self.upload_image(request), user=u)
        i.save()
        return response('Image created successfully')

    def url_request(url, data=None, headers=None):
        """Send a request"""
        request = urllib.request.Request(url=url, data=data, headers=headers)
        request_open = urllib.request.urlopen(request)
        return request_open.geturl()
