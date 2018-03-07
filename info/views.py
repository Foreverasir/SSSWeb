# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect
from models import Person,State,Warning

# Create your views here.
def state_list(requests):
    return render_to_response('sum.html',)

def uploadImg(requests):
    pass

def info_detail(requests):
    return render_to_response('sign-up.html')

def submit(requests):
    errors=[]
    if requests.method=="POST":
        if not requests.POST.get('name',''):
            errors.append("输入姓名。")
        if not requests.POST.get('address',''):
            errors.append("输入家庭住址。")
        if not requests.POST.get('ble_mac',''):
            errors.append("输入蓝牙地址。")
        if not errors:
            print(requests.POST['name'])
            p=Person.objects.filter(ble_mac=requests.POST['ble_mac'])
            if len(p)>0 :
                errors.append("该蓝牙已被使用")
            else:
                p=Person(name=requests.POST['name'],address=requests.POST['address'],birth=requests.POST['birthday'],ble_mac=requests.POST['ble_mac'])
                p.save()
                return HttpResponseRedirect('/index/')
    return render_to_response('sign-up.html',{'errors':errors})
                    
def get_head(requests):
    return render_to_response('head.html')

def get_left(requests):
    return render_to_response('left.html')

def get_index(requests):
    abnormal_state=State.objects.filter(move_flag=True)
    warnings=[]
    for s in abnormal_state:
        warning=Warning(s.person.name,s.rpi.location)
        warnings.append(warning)
    return render_to_response('index.html',{'states':State.objects.all(),'warnings':warnings})


