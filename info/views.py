# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect,JsonResponse
from models import Person,State,Warning,PersonInfo
import datetime
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
    abnormal_state=State.objects.filter(move_flag__gt=0)
    start=datetime.datetime.now()+datetime.timedelta(hours=8)-datetime.timedelta(minutes=1)
    State.objects.filter(time__lt=start).update(move_flag=2)
    warnings=[]
    for s in abnormal_state:
        warning=Warning(s.person.name,s.rpi.location)
        warnings.append(warning)
    return render_to_response('index.html',{'states':State.objects.all(),'warnings':warnings})

def ajax_list(requests):
    print("req")
    test_dict={"kobe":["room1","0"],"tracy":["room 2","1"]}
    return JsonResponse(test_dict)

def handle_person(requests):
    all=[]
    for p in Person.objects.all():
        all.append(PersonInfo(p.ble_mac,p.name,str(p.birth),p.gender,p.address))
    return render_to_response('person.html',{'person_list':all})

def add_person(requests):
    print(requests.POST)
    response={"status":True,"message":None}
    try:
        rname=requests.POST.get('name')
        rbirth=requests.POST.get('birth')
        raddress=requests.POST.get('address')
        if requests.POST.get('gender')=='true':
            rgender=True
        else:
            rgender=False
        rble_mac=requests.POST.get('ble_mac')
        check=Person.objects.filter(ble_mac=rble_mac)
        if check:
            response["status"]=False
            response["message"]="输入了已使用的蓝牙地址！"
        else:
            p=Person.objects.create(name=rname,birth=rbirth,address=raddress,gender=rgender,ble_mac=rble_mac)
            response.update(PersonInfo(rble_mac,rname,rbirth,rgender,raddress).toJson())
            #return PersonInfo(rble_mac,rname,rbirth,rgender,raddress).toJson()
    except Exception as e:
        response["status"]=False
        response["message"]="输入数据错误"
    return JsonResponse(response)