# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json,requests,re
from django.contrib.auth.hashers import make_password, check_password
from django.db import models
from shortuuidfield import ShortUUIDField
import datetime,time
from enum import Enum
from django.utils import timezone
from django.conf import settings
# Create your models here.

class Users(models.Model):
    uuid                                        =   ShortUUIDField()
    organization                                =   models.CharField(default='sunsure', max_length=128)
    username                                    =   models.CharField(default='',null=False,max_length=128)
    email                                       =   models.CharField(default='',null=False,unique=True,max_length=255)
    password                                    =   models.CharField(default='',max_length=128)
    designation                                 =   models.CharField(default='', max_length=128)     #will decide permissons.

    def set_password(self, raw_password):
        """Sets the user's password - always use this rather than directly
        assigning to :attr:`~mongoengine.django.auth.User.password` as the
        password is hashed before storage.
        """
        self.password = make_password(raw_password)
        self.save()
        return self

    def check_password(self, raw_password):
        """Checks the user's password against a provided password - always use
        this rather than directly comparing to
        :attr:`~mongoengine.django.auth.User.password` as the password is
        hashed before storage.
        """
        return check_password(raw_password, self.password)

class ProjectManagers(models.Model):
    uuid                                        =   ShortUUIDField()
    name                                        =   models.CharField(default='', max_length=256)

class Projects(models.Model):
    uuid                                        =   ShortUUIDField()
    name                                        =   models.CharField(default='', max_length=256)
    manager                                     =   models.ForeignKey(ProjectManagers,null=False)
    size                                        =   models.CharField(default='', max_length=256)
    location                                    =   models.CharField(default='', max_length=256)
    site_in_charge                              =   models.CharField(default='', max_length=256)

    def embed(self):
        return {
            'uuid':self.uuid,
            'name':self.name,
            'manager':self.manager,
            'size':self.size,
            'location':self.location,
        }

class Contractors(models.Model):
    uuid                                        =  ShortUUIDField()
    project                                     =  models.ForeignKey(Projects,null=True)
    name                                        =  models.CharField(default='', max_length=256)
    head_office                                 =  models.CharField(default='', max_length=256)
    staff_strength                              =  models.CharField(default='', max_length=256)
    expertise                                   =  models.CharField(default='', max_length=256)

    def embed(self):
        return {
            'uuid':self.uuid,
            'project_name':self.project.name,
            'name':self.name,
            'head_office':self.head_office,
            'staff_strength':self.staff_strength,
            'expertise':self.expertise,
        }

class Staff(models.Model):
    uuid                                        =  ShortUUIDField()
    project                                     =  models.ForeignKey(Projects,null=True)
    contractor                                  =  models.ForeignKey(Contractors,null=False)
    name                                        =  models.CharField(default='', max_length=256)
    dob                                         =  models.DateTimeField(default=timezone.now)
    skill                                       =  models.CharField(default='',max_length=64)
    education                                   =  models.CharField(default='',max_length=64)
    experience                                  =  models.CharField(default='',max_length=64)


    def embed(self):
        return {
            'uuid':self.uuid,
            'project_name':self.project.name,
            'name':self.name,
            'dob':self.dob.strftime('%Y-%m-%d'),
            'skill':self.skill,
            'education':self.education,
            'experience':self.experience,
        }


class Permission(models.Model):
    user                                        =   models.ForeignKey(Users)
    status                                      =   models.BooleanField(default=True)