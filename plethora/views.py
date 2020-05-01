#!/usr/bin/python
# -*- coding: utf-8 -*-
from .app import Images,Spreads,Uploads
from .content import Spreadables
from .models import Product
from feedly.core import Feedly,user

def start(request):
    e = Feedly()
    if request.method == 'GET':
        return e.start(request)

def media(request):
    u = Uploads()
    if request.method == 'GET':
        return u.media_chooser(request)

def spreaded(request):
    s = Spreadables()
    if request.method == 'GET':
        return s.view_spreaded(request)

def spreadspread(request):
    s = Spreadables()
    if request.method == 'GET':
        return s.spreadspread(request)
    elif request.method == 'POST':
        return s.spreadobject(request)

def spreadable(request):
    s = Spreadables()
    if request.method == 'GET':
        return s.view_spreadable(request)

def playable(request):
    s = Spreadables()
    if request.method == 'GET':
        return s.view_playable(request)

def imageview(request):
    s = Spreadables()
    if request.method == 'GET':
        return s.view_images(request)

def image(request):
    i = Images()
    if request.method == 'GET':
        return i.view_image(request)
    elif request.method == 'POST':
        return i.create_image(request)

def upload(request):
    u = Uploads()
    if request.method == 'GET':
        return u.view_content(request)
    elif request.method == 'POST':
        return u.upload_content(request)

def init_spread(request):
    spread = Spreads()
    if request.method == 'GET':
        return spread.start_spreadapp(request)

def main(request):
    graph = Spreads()
    if request.method == 'GET':
        return graph.view_spread(request)
    elif request.method == 'POST':
        return graph.create_spread(request)

def content(request):
    upload = Uploads()
    if request.method == 'GET':
        return upload.view_upload(request)