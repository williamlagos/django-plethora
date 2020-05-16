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

def sp(x): return '!!' in x[1]
def pl(x): return '>!' in x[1]
def im(x): return '%!' in x[1]

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