#!/usr/bin/python
# -*- coding: utf-8 -*-
from forms import CausesForm
from models import *
from coronae import append_path
from unicodedata import normalize 
append_path()

import urllib

from core.social import *
from play.models import Playable
from core.views import *

def main(request):
    proj = Project()
    if request.method == 'GET':
        return proj.view_project(request)
    elif request.method == 'POST':
        return proj.create_project(request)

def movement(request):
    group = ProjectGroup()
    if request.method == 'GET':
        return group.view_movement(request)
    elif request.method == 'POST':
        return group.create_movement(request)

class CreateHandler(Efforia):
    def get(self):
        if 'object' in self.request.arguments:
            o,t = self.request.arguments['object'][0].split(';')
            now,objs,rel = self.get_object_bydate(o,t)
            obj = globals()[objs].objects.all().filter(date=now)
            self.get_donations(obj)
        else: self.srender("create.html")
    def post(self):
        value = int(self.request.arguments['credits'][0])
        o,t = self.request.arguments['object'][0].split(';')
        now,objs,rel = self.get_object_bydate(o,t)
        obj = globals()[objs].objects.all().filter(date=now)[0]
        don = CausableDonated(value=value,donator=self.current_user(),cause=obj)
        don.save()
        self.get_donations(obj)
    def get_donations(self,cause):
        donations = list(CausableDonated.objects.all().filter(cause=cause))
        self.render_grid(donations)
        

class Project(Efforia,TwitterHandler):
    # TODO: Fazer ponte entre request handlers do Tornado e Django
    def __init__(self): pass
    def view_project(self,request):
        if 'view' in request.GET:
            strptime,token = request.GET['object'].split(';')
            now,obj,rel = self.get_object_bydate(strptime,token)
            spreaded = globals()[rel].objects.all().filter(date=now)[0]
            feed = []; feed.append(spreaded.spreaded)
            spreads = globals()[rel].objects.all().filter(spreaded=spreaded.spreaded)
            for s in spreads: feed.append(s.spread)
            self.render_grid(feed)
        else:
            form = CausesForm()
            form.fields['title'].label = 'Título do projeto'
            form.fields['content'].initial = 'Descreva o que você pretende atingir neste projeto, de uma forma bastante breve.'
            form.fields['end_time'].label = 'Prazo final'
            return render(request,"causes.html",{'form':form},content_type='text/html')
    def create_project(self,request):
        credit = int(request.POST['credit'][0])
        token = '%s' % request.POST['token']
        name = u'%s' % request.POST['title']
        title = "#%s" % name.replace(" ","")
        text = u"%s " % request.POST["content"]
        video = Playable.objects.all().filter(token=token)[0]
        end_time = datetime.strptime(request.POST['deadline'],'%d/%m/%Y')
        cause = Causable(name='#'+name,user=self.current_user(),play=video,content=text,end_time=end_time,credit=credit)
        cause.save()
        twitter = self.current_user().profile.twitter_token
        if not twitter: twitter = get_offline_access()['twitter_token']
        token = self.format_token(twitter)
        self.twitter_request(path="/statuses/update",access_token=token,
                             callback=self.async_callback(self.on_post),post_args={"status": text+title})
        causes = Causable.objects.all().filter(user=self.current_user())
        self.accumulate_points(1)
        return render(request,'grid.html',{'feed':causes},content_type='text/html')
    def on_post(self,response): self.finish()

class ProjectGroup(Efforia):
    def __init__(self): pass
    def view_movement(self,request):
        if "action" in request.GET:
            feed = []; feed.append(Action('movement'))
            causes = Causable.objects.all().filter(user=self.current_user())
            for c in causes:
                c.name = '%s#' % c.name 
                feed.append(c)
            self.render_grid(feed)
        elif 'view' in request.GET:
            move = Movement.objects.all(); feed = []; count = 0
            if 'grid' in request.GET['view']:
                for m in move.values('name').distinct():
                    if not count: feed.append(Action('new##'))
                    feed.append(move.filter(name=m['name'],user=self.current_user())[0])
                    count += 1
            else:
                name = '##%s' % request.GET['title'][0]
                feed.append(Action('play'))
                for m in move.filter(name=name,user=self.current_user()): feed.append(m.cause)
            self.render_grid(feed)
        else: 
            #move = Movement.objects.all().filter(user=self.current_user())
            move = []
            message = ""
            if not len(move):
                message = "Você não possui nenhum movimento. Gostaria de criar um?"
            else:
                scheds = len(Movement.objects.filter(user=self.current_user()).values('name').distinct())
                message = '%i Movimentos em aberto' % scheds
            return render(request,'message.html',{'message':message,'visual':'crowd.png','tutor':'Os movimentos são uma forma fácil de acompanhar todas as causas do Efforia em que você apoia. Para utilizar, basta selecioná-las e agrupá-las num movimento.'})
    def create_movement(self,request):
        causables = []
        objects = self.get_argument('objects')
        title = self.get_argument('title')
        objs = urllib.unquote_plus(objects).split(',')
        for o in objs: 
            strptime,token = o.split(';')
            now,obj,rel = self.get_object_bydate(strptime,token)
            causables.append(globals()[obj].objects.all().filter(date=now)[0])
        for c in causables: 
            move = Movement(user=self.current_user(),cause=c,name='##'+title)
            move.save()
        self.accumulate_points(1)
        moves = len(Movement.objects.all().filter(user=self.current_user()).values('name').distinct())
        return self.srender('message.html',message='%i Movimentos em aberto' % moves,visual='crowd.png',tutor='Os movimentos são uma forma fácil de acompanhar todas as causas do Efforia em que você apoia. Para utilizar, basta selecioná-las e agrupá-las num movimento.')
