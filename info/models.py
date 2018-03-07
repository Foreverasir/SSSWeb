# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
'''用户：
    姓名，地址，
'''
class Person(models.Model):
    name=models.CharField(max_length=30)
    address=models.CharField(max_length=50)
    birth=models.DateField()
    ble_mac=models.CharField(max_length=30,primary_key=True)

    def __unicode__(self):
        return self.name

class Rpi(models.Model):
    ip=models.CharField(max_length=30,default="192.1.2.105",primary_key=True)
    location=models.CharField(max_length=20,default="001")

    def __unicode__(self):
        return self.ip

class Sensortag(models.Model):
    person=models.ForeignKey(Person)

    rpi=models.ForeignKey(Rpi)

    light=models.FloatField()

    acc_x=models.FloatField()
    acc_y=models.FloatField()
    acc_z=models.FloatField()

    gyro_x=models.FloatField()
    gyro_y=models.FloatField()
    gyro_z=models.FloatField()

    magn_x=models.FloatField()
    magn_y=models.FloatField()
    magn_z=models.FloatField()

    move_flag=models.BooleanField(default=False)

    def __unicode__(self):
        return "adsa"

class State(models.Model):
    person=models.ForeignKey(Person)
    rpi=models.ForeignKey(Rpi)
    move_flag=models.BooleanField(default=False)

    def __unicode__(self):
        return self.move_flag

class Warning:
    def __init__(self,name,location):
        self.name=name
        self.location=location