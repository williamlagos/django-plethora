#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests,json,urllib,urllib2,re,oauth2 as oauth
from datetime import datetime
from time import mktime,strptime
from django.contrib.auth.models import User
from django.http import HttpResponse as response
from django.http import HttpResponseRedirect as redirect
from django.shortcuts import render
from django.db import IntegrityError

from models import *
from main import Efforia
from files import Dropbox

class Search(Efforia):
    def __init__(self): pass
    def explore(self,request):
        try: query = request.GET['explore']
        except KeyError,e: query = ''
        u = self.current_user(request)
        others = [x['id'] for x in Profile.objects.values('id')]
        objects = self.feed(u,others)
        filter(lambda obj: query.lower() in obj.name.lower(),objects)
        return self.view_mosaic(request,objects)

class Follows(Efforia):
    def __init__(self): pass
    def view_following(self,request):
        u = self.current_user(request); rels = []
        for f in Followed.objects.filter(follower=u.id):
            rels.append(Profile.objects.filter(id=f.followed)[0])
        return self.view_mosaic(request,rels)
    def become_follower(self,request):
        u = self.current_user(request).id
        followed = Profile.objects.filter(id=request.GET['profile_id'])[0].user_id
        follow = Followed(followed=followed,follower=u)
        follow.save()
        return response('Profile followed successfully')
    def leave_follower(self,request):
        u = self.current_user(request).id
        followed = request.GET['profile_id']
        query = Followed.objects.filter(followed=followed,follower=u)
        if len(query): query[0].delete()
        return response('Profile unfollowed successfully')


class ID(Efforia):
    def __init__(self): pass
    def view_id(self,request):
        u = self.current_user(request)
        if 'first_turn' in request.GET:
            if u.profile.first_turn: return response('yes')
            else: return response('no')
        elif 'object' in request.GET:
            o,t = request.GET['object'][0].split(';')
            now,objs,rels = self.get_object_bydate(o,t)
            obj = globals()[objs].objects.all().filter(date=now)[0]
            if hasattr(obj,'user'): return response(str(obj.user.id))
            else: return response(str(self.current_user().id))
        else: return response(str(self.current_user().id))
    def finish_tutorial(self,request):
        u = self.current_user(request)
        p = Profile.objects.all().filter(user=u)[0]
        p.first_time = False
        p.save()
        return response('Tutorial finalizado.')

class Deletes(Efforia):
    def delete_element(self,request):
        objects = settings.EFFORIA_OBJS
        oid = request.GET['id']
        obj = self.object_token(request.GET['token'])[0]
        for app,appmodels in objects.iteritems():
            for m in appmodels:
                if obj in m: module = '%s.models'%app; break
        o = self.class_module(module,obj)
        query = o.objects.filter(id=oid)
        if len(query): query[0].delete()
        return response('Object deleted successfully')

class Tutorial(Efforia):
    def view_tutorial(self,request):
        username = full_name = ''; social = False
        if 'social' in request.GET:
            social = True; username = request.COOKIES['username']
            full_name = User.objects.filter(username=username)[0].get_full_name()
        return render(request,'tutorial.pug',{'static_url':settings.STATIC_URL,'social':social,'username':username,'fullname':full_name})
    def create_profile(self,request,url,user):
        birthday = career = bio = ''
        for k,v in request.POST.iteritems():
            if 'birth' in k: birthday = self.convert_datetime(v)
            elif 'career' in k: career = v
            elif 'bio' in k: bio = v
        profile = Profile(user=user,birthday=birthday,bio=bio,career=career)
        profile.save()
        return redirect(url)
    def finish_tutorial(self,request):
        whitespace = ' '
        data = request.POST
        name = request.COOKIES['username']
        u = User.objects.filter(username=name)[0]
        if len(data['usern']) > 0: u.username = name = data['usern']
        if len(data['passw']) > 0:
            password = data['passw']
            u.set_password(password)
        if len(data['name']) > 0:
            lname = data['name'].split()
            u.first_name,u.last_name = lname[0],whitespace.join(lname[1:])
        u.save()
        url = 'enter?username=%s&password=%s' % (name,password)
        if len(request.POST) is 0: return redirect(url)
        else: return self.create_profile(request,url,u)

class Authentication(Efforia):
    def authenticate(self,request):
        print request.GET
        data = request.GET
        if 'profile' in data:
            profile = self.json_decode(data['profile'])
            typesoc = data['social']
            # Atualizacao do perfil com tokens sociais
            if 'user' in request.session:
                u = self.current_user(request)
                p = Profile.objects.filter(user=u)[0]
                if 'google' in typesoc: p.google_token = profile['google_token']
                elif 'twitter' in typesoc: p.twitter_token = '%s;%s' % (profile['key'],profile['secret'])
                elif 'facebook' in typesoc: p.facebook_token = profile['facebook_token']
                p.save()
                return redirect('/')
            # Registro do perfil com token social
            else:
                whitespace = ' '
                if 'twitter' in typesoc:
                    first_name = profile['first_name']
                    last_name = ''
                    username = profile['screen_name']
                    token = '%s;%s' % (profile['key'],profile['secret'])
                elif 'facebook' in typesoc:
                    first_name = profile['first_name']
                    last_name = whitespace.join(re.findall('[A-Z][^A-Z]*',profile['last_name']))
                    username = profile['link'].split('/')[-1:][0]
                    token = profile['facebook_token']
                elif 'google' in typesoc:
                    first_name = profile['given_name']
                    last_name = whitespace.join(re.findall('[A-Z][^A-Z]*',profile['family_name']))
                    username = profile['name'].lower()
                    token = profile['google_token']
                u = User(username=username,password='3ff0r14',first_name=first_name,last_name=last_name)
                if len(list(User.objects.filter(username=username))) > 0:
                    request.session['user'] = username
                    return redirect('/')
                u.save()
                r = redirect('tutorial?social=%s'%data['social'])
                r.set_cookie('username',username)
                r.set_cookie('token',token)
                return r
                #return response(json.dumps(profile),mimetype='application/json')
        elif 'username' not in data or 'password' not in data:
            return response(json.dumps({'error':'User or password missing'}))
        else:
            username = data['username']
            password = data['password']
            exists = User.objects.filter(username=username)
            if exists:
                if exists[0].check_password(password):
                    obj = json.dumps({'username':username,'userid':exists[0].id})
                    request.session['user'] = username
                    return response(json.dumps({'success':'Login successful'}))
                else:
                    obj = json.dumps({'error':'User or password wrong'})
                    return response(obj)
    def leave(self,request):
        del request.session['user']
        return response(json.dumps({'success':'Logout successful'}))
    def view_register(self,request):
        return render(request,'register.pug',{'static_url':settings.STATIC_URL,'hostname':request.get_host()},content_type='text/html')
    def participate(self,request):
        whitespace = ' '
        username = password = first_name = last_name = ''
        for k,v in request.POST.iteritems():
            if 'username' in k:
                u = User.objects.filter(username=v)
                if len(u) > 0: return response('Username already exists')
                else: username = v
            elif 'password' in k:
                if v not in request.POST['repeatpassword']: return response('Password mismatch')
                else: password = v
            elif 'name' in k: first_name,last_name = whitespace.join(v.split()[:1]),whitespace.join(v.split()[1:])
        user = User(username=username,first_name=first_name,last_name=last_name)
        user.set_password(password)
        user.save()
        r = redirect('tutorial')
        r.set_cookie('username',username)
        return r

class Twitter(Efforia):
    def update_status(self,request):
        u = self.current_user(request)
        if len(request.GET['content']) > 137:
            short = unicode('%s...' % (request.GET['content'][:137]))
        else: short = unicode('%s' % (request.GET['content']))
        tokens = u.profile.twitter_token
        if not tokens: tokens = self.own_access()['twitter_token']
        data = {'status':short.encode('utf-8')}
        self.oauth_post_request('/statuses/update.json',tokens,data,'twitter')
        return response('Published posting successfully on Twitter')

class Facebook(Efforia):
    def update_status(self,request):
        u = self.current_user(request)
        token = u.profile.facebook_token
        text = unicode('%s' % request.GET['content'])
        data = {'message':text.encode('utf-8')}
        if 'id' in request.GET: url = '/%s/feed' % request.GET['id']
        else: url = '/me/feed'
        self.oauth_post_request(url,token,data,'facebook')
        return response('Published posting successfully on Facebook')
    def send_event(self,request):
        u = self.current_user(request)
        token = u.profile.facebook_token
        name = dates = descr = local = ''
        for k,v in request.GET.iteritems():
            if 'name' in k: name = v
            elif 'deadline' in k: dates = v
            elif 'description' in k: descr = v.encode('utf-8')
            elif 'location' in k: local = v.encode('utf-8')
        date = self.convert_datetime(dates)
        url = 'http://www.efforia.com.br/%s/promote/enroll?name=%s'%(request.get_host(),name)
        data = {'name':name,'start_time':date,'description':descr,'location':local,'ticket_uri':url}
        id = json.loads(self.oauth_post_request("/me/events",token,data,'facebook'))['id']
        return response(id)
    def send_event_cover(self,request):
        u = self.current_user(request)
        token = u.profile.facebook_token
        ident = request.POST['id']
        photo = request.POST['url']
        self.oauth_post_request('/%s'%ident,token,{'cover_url':photo},'facebook')
        return response('Published image cover on event successfully on Facebook')

class Coins(Efforia):
    def discharge(self,request):
        userid = request.GET['userid']
        values = request.GET['value']
        u = Profile.objects.filter(user=(userid))[0]
        u.credit -= int(values)
        u.save()
        j = json.dumps({'objects':{
            'userid':userid,
            'value':u.credit
        }})
        return response(j)
    def recharge(self,request):
        userid = request.GET['userid']
        values = request.GET['value']
        u = Profile.objects.filter(user=(userid))[0]
        u.credit += int(values)
        u.save()
        json.dumps({'objects':{
            'userid': userid,
            'value': u.credit
        }})
        return response(j)
    def balance(self,request):
        userid = request.GET['userid']
        json.dumps({'objects':{
            'userid': userid,
            'value': Profile.objects.filter(user=int(userid))[0].credit
        }})
        return response(j)
