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
from .app import Plethora

class Spreadables(Plethora):
    def __init__(self): pass
    def view_spreadable(self,request):
        spread_id = int(request.GET['id'])
        s = Spreadable.objects.filter(id=spread_id)[0]
        return render(request,'spreadview.pug',{'content':s.content,'spreadid':spread_id},content_type='text/html')
    def view_playable(self,request):
        playable_id = int(request.GET['id'])
        e = Playable.objects.filter(id=playable_id)[0]
        return render(request,'videoview.pug',{'playableid':playable_id},content_type='text/html')
    def view_images(self,request):
        image_id = int(request.GET['id'])
        i = Image.objects.filter(id=image_id)[0]
        return render(request,'imageview.pug',{'description':i.description,'image':i.link,'imageid':image_id},content_type='text/html')
    def spreadspread(self,request):
        return render(request,'spread.pug',{'id':request.GET['id']},content_type='text/html')
    def spreadobject(self,request):
        u = self.current_user(request)
        c = request.POST['content']
        spread = Spreadable(user=u,content=c,name='!'+u.username)
        spread.save()
        objid = request.POST['id']
        token = request.POST['token']
        s = Spreaded(name=token,spread=objid,spreaded=spread.id,user=u)
        s.save()
        return response('Spreaded object created successfully')
    def view_spreaded(self,request):
        spreadables = []; u = self.current_user(request)
        objid = request.GET['spreaded_id']
        token = request.GET['spreaded_token']
        typ,rel = self.object_token(token)
        sprdd = globals()[rel].objects.filter(spread=objid,name=token+'!')
        spreadables.append(globals()[typ].objects.filter(id=sprdd[0].spread)[0])
        for s in sprdd: spreadables.append(Spreadable.objects.filter(id=s.spreaded)[0])
        return self.view_mosaic(request,spreadables)
