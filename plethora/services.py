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

from django.shortcuts import render
from django.http import HttpResponse as response

from .models import Spreadable,Image,Playable,Spreaded
# from .providers import *

class ContentService:

    model = Spreadable

    def __init__(self): 
        pass

    def start(self, request):
        if 'user' in request.session:
            # Painel do usuario
            u = user(request.session['user'])
            names = settings.EFFORIA_NAMES; apps = []
            for a in settings.EFFORIA_APPS: apps.append(names[a])
            return render(request,'index.pug',{'static_url':settings.STATIC_URL,
                                                'user':user(request.session['user']),
                                                'name':'%s %s' % (u.first_name,u.last_name),'apps':apps
                                                },content_type='text/html')
        # Pagina inicial
        p = list(Page.objects.filter(user=superuser()))
        return render(request,'index.html',{'static_url':settings.STATIC_URL,'pages':p,},content_type='text/html')

    def external(self, request):
        u = self.current_user(request)
        sellables = Sellable.objects.filter(user=u)
        for s in sellables: s.paid = True
        return self.redirect('/')

    def json_decode(self, string):
        j = json.loads(string,'utf-8')
        return ast.literal_eval(j)

    def url_request(self, url, data=None, headers={}):
        request = urllib.request.Request(url=url,data=data,headers=headers)
        request_open = urllib.request.urlopen(request)
        return request_open.geturl()

    def do_request(self, url, data=None, headers={}):
        request = urllib.request.Request(url=url,data=data,headers=headers)
        try:
            request_open = urllib.request.urlopen(request)
            response = request_open.read()
            request_open.close()
        except urllib.error.HTTPError as e:
            print(url)
            print(data)
            print(headers)
            print(e.code)
            print(e.msg)
            print(e.hdrs)
            print(e.fp)
        return response

    def object_token(self, token):
        relations = settings.EFFORIA_TOKENS
        typobject = relations[token]
        return typobject

    def object_byid(self, token, ident):
        obj = self.object_token(token)
        return globals()[obj].objects.filter(id=ident)[0]

    def convert_datetime(self, date_value):
        d = time.strptime(date_value,'%d/%m/%Y')
        return datetime.fromtimestamp(time.mktime(d))

    def authenticate(self, username, password):
        exists = User.objects.filter(username=username)
        if exists:
            if exists[0].check_password(password):
                return exists
        else: return None

    def authenticated(self):
        name = self.get_current_user()
        if not name:
            #self.redirect('login')
            self.render('templates/enter.html',STATIC_URL=settings.STATIC_URL)
            return False
        else:
            return True

    def accumulate_points(self, points, request=None):
        if request is None: u = self.current_user()
        else: u = self.current_user(request)
        current_profile = Profile.objects.all().filter(user=u)[0]
        current_profile.points += points
        current_profile.save()

    def view_spreadable(self, request):
        spread_id = int(request.GET['id'])
        s = Spreadable.objects.filter(id=spread_id)[0]
        return render(request,'spreadview.pug',{'content':s.content,'spreadid':spread_id},content_type='text/html')

    def view_playable(self, request):
        playable_id = int(request.GET['id'])
        e = Playable.objects.filter(id=playable_id)[0]
        return render(request,'videoview.pug',{'playableid':playable_id},content_type='text/html')

    def view_images(self, request):
        image_id = int(request.GET['id'])
        i = Image.objects.filter(id=image_id)[0]
        return render(request,'imageview.pug',{'description':i.description,'image':i.link,'imageid':image_id},content_type='text/html')

    def spreadspread(self, request):
        return render(request,'spread.pug',{'id':request.GET['id']},content_type='text/html')

    def spreadobject(self, request):
        u = self.current_user(request)
        c = request.POST['content']
        spread = Spreadable(user=u,content=c,name='!'+u.username)
        spread.save()
        objid = request.POST['id']
        token = request.POST['token']
        s = Spreaded(name=token,spread=objid,spreaded=spread.id,user=u)
        s.save()
        return response('Spreaded object created successfully')

    def view_spreaded(self, request):
        spreadables = []; u = self.current_user(request)
        objid = request.GET['spreaded_id']
        token = request.GET['spreaded_token']
        typ,rel = self.object_token(token)
        sprdd = globals()[rel].objects.filter(spread=objid,name=token+'!')
        spreadables.append(globals()[typ].objects.filter(id=sprdd[0].spread)[0])
        for s in sprdd: spreadables.append(Spreadable.objects.filter(id=s.spreaded)[0])
        return self.view_mosaic(request,spreadables)

    def start_spreadapp(self, request):
        return render(request,'spreadapp.pug',{'static_url':settings.STATIC_URL},content_type='text/html')

    def view_spread(self, request):
        return render(request,"spread.pug",{},content_type='text/html')

    def create_spread(self, request):
        u = self.current_user(request)
        name = u.first_name.lower()
        text = str('%s' % (request.POST['content']))
        post = Spreadable(user=u,content=text,name='!'+name)
        post.save()
        self.accumulate_points(1,request)
        return response('Spreadable created successfully')

    def deadline(self):
        playables = Playable.objects.filter(user=self.user)
        for play in playables:
            if not play.token and not play.visual: play.delete()

    def relations(self, feed):
        excludes = []; rels = Spreaded.objects.filter(user=self.user)
        excludes.extend([(r.spreaded,'!!') for r in rels])
        excludes.extend([(r.spread,r.token()) for r in rels])
        for v in rels.values('spread').distinct():
            t = rels.filter(spread=v['spread'],user=self.user)
            if len(t) > 0: feed.append(t[len(t)-1])
        return excludes

    def duplicates(self, exclude, feed):
        for o in self.objects:
            objects = globals()[o].objects.filter(user=self.user)
            if 'Spreadable' in o: e = list(filter(sp,exclude))
            elif 'Playable' in o: e = list(filter(pl,exclude))
            elif 'Image' in o: e = list(filter(im,exclude))
            excludes = [x[0] for x in e]
            feed.extend(objects.exclude(id__in=excludes))

    # def __init__(self,user,app):
    #     Activity.__init__(self,user,app)