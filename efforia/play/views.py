#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
from handlers import append_path
from stream import StreamService
append_path()

import tornado.web,re
from tornado import httpclient
from models import *
from unicodedata import normalize
from create.models import Causable
from spread.views import SocialHandler
from core.models import Profile
from StringIO import StringIO

class CollectionHandler(SocialHandler):
    def get(self):
        if not self.authenticated(): return
        self.render(self.templates()+'collection.html')

class FeedHandler(SocialHandler):
    def get(self):
        if not self.authenticated(): return
        service = StreamService()
        feed = service.top_rated()
        return self.render(self.templates()+'play.html',feed=feed)
    def post(self):
        token = self.parse_request(self.request.body)
        service = StreamService()
        feed = service.top_rated()
        return self.srender('play.html',feed=feed,token=token)

class ContentHandler(SocialHandler):
    def get(self):
        self.srender("contents.html")

class UploadHandler(SocialHandler):
    def get(self):
        if not self.authenticated(): return
        description = ''; token = '!!'
        for k in self.request.arguments.keys(): description += '%s;;' % self.request.arguments[k][0]
        t = token.join(description[:-2].split())
        self.clear_cookie('description')
        self.set_cookie('description',t)
    def post(self):
        content = re.split(';;',self.get_cookie('description').replace('!!',' ').replace('"',''))
        text,keywords,category,title = content
        category = int(category); keys = ','
        keywords = keywords.split(' ')
        for k in keywords: k = normalize('NFKD',k.decode('utf-8')).encode('ASCII','ignore')
        keys = keys.join(keywords)
        service = StreamService()
        response = service.video_entry(title,text,keys)
        video_io = StringIO()
        video = self.request.files['Filedata'][0]
        video_io.write(video['body'])
        resp = service.insert_video(response,video_io,video["content_type"])
        self.accumulate_points(3)
        token = resp.GetSwfUrl().split('/')[-1:][0].split('?')[0]
        playable = Playable(user=self.current_user(),name='>'+title+';'+keys,description=text,token=token,category=category)
        playable.save()
        self.set_cookie('token',token)
        self.write(token)

class ScheduleHandler(SocialHandler):
    def get(self):
        if "action" in self.request.arguments:
            play = Playable.objects.all().filter(user=self.current_user)
            self.srender('schedule.html',play=play)
        else: 
            play = Schedule.objects.all().filter(user=self.current_user)
            message = ""
            if not len(play):
                message = "Você não possui nenhuma programação no momento. Gostaria de criar uma?"
            else:
                scheds = len(Schedule.objects.filter(user=self.current_user()).values('name').distinct())
                message = '%i Programações de vídeos disponíveis' % scheds
            self.srender('message.html',message=message)
    def post(self):
        playables = []
        objects = self.get_argument('objects')
        title = self.get_argument('title')
        objs = urllib.unquote_plus(str(objects)).split(',')
        for o in objs: playables.append(Playable.objects.all().filter(token=o)[0])
        for p in playables: 
            playsched = Schedule(user=self.current_user(),play=p,name='>>'+title)
            playsched.save()
        scheds = len(Schedule.objects.all().filter(user=self.current_user(),name=title))
        self.srender('message.html',message='%i Programações de vídeos disponíveis' % scheds)
