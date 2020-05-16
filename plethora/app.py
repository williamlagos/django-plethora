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

import re

from unicodedata import normalize
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse as response
from django.http import HttpResponseRedirect as redirect
from django.conf import settings

from .models import Spreadable,Image,Playable,Spreaded#,Profile

def sp(x): return '!!' in x[1]
def pl(x): return '>!' in x[1]
def im(x): return '%!' in x[1]

class DropboxExternalProvider:

    def __init__(self): 
        pass

    def view_image(self, request):
        return render(request,'image.pug',{'static_url':settings.STATIC_URL},content_type='text/html')

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
        i = Image(link=self.upload_image(request),user=u)
        i.save()
        return response('Image created successfully')

class YouTubeExternalProvider:

    def __init__(self): 
        pass

    def view_upload(self, request):
        return render(request,'content.pug',{'static_url':settings.STATIC_URL},content_type='text/html')

    def set_thumbnail(self, request):
        u = self.current_user(request)
        service = StreamService()
        token = request.GET['id']
        access_token = u.profile.google_token
        thumbnail = service.video_thumbnail(token,access_token)
        play = Playable.objects.filter(user=u).latest('date')
        play.visual = thumbnail
        play.token = token
        play.save()
        self.accumulate_points(1,request)
        r = redirect('/')
        r.set_cookie('token',token)
        return r

    def view_content(self, request):
        u = self.current_user(request)
        content = title = ''
        for k,v in request.REQUEST.items():
            if 'title' in k: title = v
            elif 'content' in k: content = v
            elif 'status' in k:
                return self.set_thumbnail(request)
        try:
            url,token = self.parse_upload(request,title,content)
            return render(request,'video.pug',{'static_url':settings.STATIC_URL,
                                                  'hostname':request.get_host(),
                                                  'url':url,'token':token},content_type='text/html')
        except Exception: return response('Invalid file for uploading')

    def parse_upload(self, request, title, content):
        keys = ','; keywords = content.split(' ')
        for k in keywords: k = normalize('NFKD',k.decode('utf-8')).encode('ASCII','ignore')
        keys = keys.join(keywords)
        playable = Playable(user=self.current_user(request),name='>'+title,description=content)
        playable.save()
        service = StreamService()
        access_token = self.current_user(request).profile.google_token
        return service.video_entry(title,content,keys,access_token)

    def media_chooser(self, request):
        return render(request,'chooser.pug')

class DefaultExternalProvider:

    def oauth_post_request(self, url, tokens, data={}, social='twitter', headers={}):
        api = json.load(open('settings.json','r'))['social']
        posturl ='%s%s'%(api[social]['url'],url)
        if 'facebook' in social:
            socialurl = '%s?%s'%(posturl,urllib.parse.urlencode({'access_token':tokens}))
            if 'start_time' in data: data['start_time'] = data['start_time'].date()
            return self.do_request(socialurl,urllib.parse.urlencode(data),headers)
        else:
            access_token,access_token_secret = tokens.split(';')
            token = oauth.Token(access_token,access_token_secret)
            consumer_key = api[social]['client_key']
            consumer_secret = api[social]['client_secret']
            consumer = oauth.Consumer(consumer_key,consumer_secret)
            client = oauth.Client(consumer,token)
            try:
                return client.request(posturl,'POST',urllib.parse.urlencode(data))
            except urllib.error.HTTPError as e:
                print(e.code)
                print(e.msg)
                print(e.hdrs)
                print(e.fp)
                return 1

    def refresh_google_token(self, token):
        api = json.load(open('settings.json','r'))['social']['google']
        if not token: token = self.own_access()['google_token']
        data = urllib.parse.urlencode({
            'client_id':      api['client_id'],
            'client_secret':  api['client_secret'],
            'refresh_token':  token,
            'grant_type':    'refresh_token' })
        return json.loads(self.do_request(api['oauth2_token_url'],data))['access_token']

    def own_access(self):
        objs = json.load(open('settings.json','r'))
        google_api = objs['social']['google']
        twitter_api = objs['social']['twitter']
        facebook_api = objs['social']['facebook']
        access = {
            'google_token': google_api['client_token'],
            'twitter_token': '%s;%s' % (twitter_api['client_token'],twitter_api['client_token_secret']),
            'facebook_token': facebook_api['client_token']
        }
        return access