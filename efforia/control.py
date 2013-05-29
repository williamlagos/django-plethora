import json,time
from datetime import datetime
from django.contrib.auth.models import User
from django.http import HttpResponse as response
from django.conf import settings
from django.shortcuts import render

from models import Profile,Followed,Place
from files import Dropbox
from main import Efforia

class Control(Efforia):
    def __init__(self): pass
    def view_panel(self,request):
        return render(request,'configapp.jade',{'static_url':settings.STATIC_URL},content_type='text/html')
    def view_integrations(self,request):
        return render(request,'integrations.jade',{'session':request.COOKIES['sessionid'],
                                                   'hostname':request.get_host(),
                                                   'static_url':settings.STATIC_URL},content_type='text/html')
    def view_control(self,request):
        p = Profile.objects.filter(user=self.current_user(request))[0]
        return render(request,'appearance.jade',{
                                                 'static_url':settings.STATIC_URL,
                                                 'interface':p.interface,
                                                 'typeditor':p.typeditor,
                                                 'language':p.language,
                                                 'monetize':p.monetize },content_type='text/html')
    def view_options(self,request):
        p = Profile.objects.filter(user=self.current_user(request))[0]
        value = 0
        for k,v in request.GET.items():
            if 'interface' in k:
                value = p.interface
            elif 'typeditor' in k:
                value = p.typeditor
            elif 'language' in k:
                value = p.language
            elif 'monetize' in k:
                value = p.monetize
        return response(value)
    def change_control(self,request):
        p = Profile.objects.filter(user=self.current_user(request))[0]
        for k,v in request.POST.items():
            if 'interface' in k:
                p.interface = int(v)
            elif 'typeditor' in k:
                p.typeditor = int(v)
            elif 'language' in k:
                p.language = int(v)
            elif 'monetize' in k:
                p.monetize = int(v)
        p.save()
        return response('Settings changed successfully')

class Photos(Efforia):
    def __init__(self): pass
    def view_photo(self,request):
        return render(request,'photo.jade',{'static_url':settings.STATIC_URL},content_type='text/html')
    def change_photo(self,request):
        p = Profile.objects.filter(user=self.current_user(request))[0]
        photo = request.FILES['Filedata'].read()
        dropbox = Dropbox()
        link = dropbox.upload_and_share(photo)
        res = self.url_request(link)
        url = '%s?dl=1' % res
        p.visual = url
        p.save()
        return response('Photo changed successfully')

class Passwords(Efforia):
    def __init__(self): pass
    def view_password(self,request):
        return render(request,'password.jade',{'password':''},content_type='text/html')
    def change_password(self,request):
        user = self.current_user(request)
        old = request.POST['old_password']
        new1 = request.POST['new_password1']
        new2 = request.POST['new_password2']
        if not user.check_password(old): 
            return response('Senha incorreta.')
        user.set_password(new1)
        user.save()
        return response('Senha alterada!')

class Profiles(Efforia):
    def __init__(self): pass
    def view_profile(self,request):
        user = self.current_user(request)
        return render(request,'profile.jade',{
                                                'static_url':settings.STATIC_URL,
                                                'profile':user.profile,
                                                'name':user.first_name.encode('utf-8'),
                                                'sname':user.last_name.encode('utf-8'),
                                                'birth':user.profile.birthday.strftime('%d/%m/%Y')
                                                },content_type='text/html')
    def update_profile(self,request):
        user = self.current_user(request)
        for key,value in request.POST.items():
            if len(value) is 0: continue
            elif 'user' in key: 
                user.username = value
                self.set_current_user(request,value)
            elif 'email' in key: user.email = value
            elif 'name' in key: user.first_name = value
            elif 'lastn' in key: user.last_name = value
            elif 'birth' in key: 
                strp_time = time.strptime(value,"%d/%m/%Y")
                profile = self.current_user(request).profile
                profile.birthday = datetime.fromtimestamp(time.mktime(strp_time))
                profile.save()
            user.save()
        return response('Profile updated successfully')
    def view_userinfo(self,request):
        nothimself = True; followed = False
        current = self.current_user(request)
        u = Profile.objects.filter(id=request.GET['profile_id'])[0].user
        f = Followed.objects.filter(followed=u.id,follower=current.id)
        if u.id == current.id: nothimself = False
        if len(f) > 0: followed = True
        return render(request,'profileview.jade',{'profile':u.profile,
                                                  'nothimself':nothimself,
                                                  'followed':followed},content_type='text/html')
    def view_activity(self,request):
        u = Profile.objects.filter(id=request.GET['profile_id'])[0].user
        profile_objects = self.feed(u)
        return self.view_mosaic(request,profile_objects,u.profile)

class Places(Efforia):
    def __init__(self): pass
    def register_place(self,request):
        u = self.current_user(request)
        exists = len(Place.objects.filter(user=u))
        return render(request,'place.jade',{'exists':exists,'user':u},content_type='text/html')
    def create_place(self,request):
        u = self.current_user(request)
        country = city = code = ''
        for k,v in request.POST.items():
            if 'country' in k: country = v
            elif 'city' in k: city = v
            elif 'code' in k: code = v.replace('-','').replace(' ','')
        place = Place.objects.filter(user=u)
        if len(place): 
            p = place[0]
            p.country = country
            p.city = city
            p.code = code
            p.save()
        else:
            p = Place(user=u,country=country,city=city,code=code)
            p.save() 
        return response('Place created/updated sucessfully')
