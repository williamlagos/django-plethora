#!/usr/bin/python
# -*- coding: utf-8 -*-
from django_pagseguro.pagseguro import CarrinhoPagSeguro,ItemPagSeguro
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.widgets import ValueHiddenInput, ReservedValueHiddenInput
from django.shortcuts import render
from django.conf import settings
from django import forms
from models import Sellable,Basket,user
from feed import Mosaic

class Baskets(Mosaic):
    def __init__(self,sellobj=Sellable):
        self.sellable = sellobj
    def view_items(self,request):
        u = self.current_user(request); products = []
        basket = list(Basket.objects.filter(user=u))
        for b in basket: products.extend(self.sellable.objects.filter(sellid=b.product))
        return self.view_mosaic(request,products)
    def add_item(self,request):
        u = self.current_user(request)
        prodid = int(request.REQUEST['id'])
        if 'value' in request.REQUEST:
            value = request.REQUEST['value']
            token = request.REQUEST['token']
            s = self.sellable(user=u,name=token,value=value,sellid=prodid)
            s.save()
        exists = Basket.objects.all().filter(user=u,product=prodid)
        if not len(exists):
            basket = Basket(user=u,product=prodid)
            basket.save()
        return self.view_items(request)
    def process_cart(self,request):
        u = user(request.session['user']); cart = []
        basket = list(Basket.objects.filter(user=u))
        for b in basket:
            sellables = Sellable.objects.filter(sellid=b.product)
            for s in sellables:
                prod = {}
                prod['value'] = s.value
                prod['product'] = s.name
                prod['qty'] = '1'
                cart.append(prod)
        return self.process(request,cart)
    def process(self,request,cart=None):
        pass

class PagSeguro(Baskets):
    def process(self,request,cart=None):
    	for k,v in request.REQUEST.iteritems():
	    if 'product' in k: product = v
	    elif 'value' in k: value = float(v)
	    elif 'qty' in k: qty = int(v)
        carrinho = CarrinhoPagSeguro(ref_transacao=1); count = 0
        if cart is not None:
            for p in cart:
                count += 1
                carrinho.add_item(ItemPagSeguro(cod=count,descr=p['product'],quant=p['qty'],valor=p['value']))
        else:
            carrinho.add_item(ItemPagSeguro(cod=1,descr=product,quant=qty,valor=value))
        form_pagseguro = carrinho.form()
        return render(request,'form.jade',{'form':form_pagseguro})

class PayPal(Baskets):
    def process(self,request,cart=None):
    	for k,v in request.REQUEST.iteritems():
	    if 'product' in k: product = v
	    elif 'value' in k: value = float(v)
	    elif 'qty' in k: qty = int(v)
        paypal = {
            'business':      settings.PAYPAL_RECEIVER_EMAIL,
            'notify_url':    settings.PAYPAL_NOTIFY_URL,
            'return_url':    settings.PAYPAL_RETURN_URL,
            'cancel_return': settings.PAYPAL_CANCEL_RETURN,
            'currency_code': 'BRL',
        }
        option = '_cart'; count = 0
        form_paypal = PayPalPaymentsForm(initial=paypal)
        if cart is not None:
            for p in cart:
                count += 1
                form_paypal.fields['amount_%i'%count] = forms.IntegerField(widget=ValueHiddenInput(),initial=p['value'])
                form_paypal.fields['item_name_%i'%count] = forms.CharField(widget=ValueHiddenInput(),initial=p['product'])
                form_paypal.fields['quantity_%i'%count] = forms.CharField(widget=ValueHiddenInput(),initial=p['qty'])
        else:
            form_paypal.fields['amount_1'] = forms.IntegerField(widget=ValueHiddenInput(),initial=value)
            form_paypal.fields['item_name_1'] = forms.CharField(widget=ValueHiddenInput(),initial=product)
            form_paypal.fields['quantity_1'] = forms.CharField(widget=ValueHiddenInput(),initial=str(qty))
        form_paypal.fields['cmd'] = forms.CharField(widget=ValueHiddenInput(),initial=option)
        form_paypal.fields['upload'] = forms.CharField(widget=ValueHiddenInput(),initial='1')
	return render(request,'form.jade',{'form':form_paypal.render()})
