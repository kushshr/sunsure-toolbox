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

class TestStatus(Enum):   # A subclass of Enum
    RUNNING = 0
    COMPLETED = 1
    ABORTED = -1

class Organization(models.Model):
    uuid                                        =   ShortUUIDField()
    name                                        =   models.CharField(default='',max_length=128)
    website_url                                 =   models.CharField(default='',max_length=128)
    created_at                                  =   models.DateTimeField(default=timezone.now)

class Users(models.Model):
    uuid                                        =   ShortUUIDField()
    organization                                =   models.CharField(default='sunsure')
    username                                    =   models.CharField(default='',null=False,max_length=128)
    email                                       =   models.CharField(default='',null=False,unique=True,max_length=255)
    password                                    =   models.CharField(default='',max_length=128)
    designation                                 =   models.CharField(default='')

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
    name                                        =   models.CharField(default='')

    def __init__(self,name=''):
        self.name = ''

class Projects(models.Model):
    uuid                                        =   ShortUUIDField()
    name                                        =   models.CharField(default='')
    manager                                     =   models.ForeignKey(ProjectManagers,null=False)
    size                                        =   models.CharField(default='')
    location                                    =   models.CharField(default='')
    site_in_charge                              =   models.CharField(default='')

    def __init__(self, name = '', manager='', size='', location='', site_in_charge=''):
        self.name = name
        self.manager = manager
        self.size  = size
        self.location = location
        self.site_in_charge = site_in_charge


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
    project                                     =  models.ForeignKey(Project,null=True)
    name                                        =  models.CharField(default='')
    head_office                                 =  models.CharField(default='')
    staff_strength                              =  models.CharField(default='')
    expertise                                   =  models.CharField(default='')

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
    project                                     =  models.ForeignKey(Project,null=True)
    contractor                                  =  models.ForeignKey(Contractors,null=False)
    name                                        =  models.CharField(default='')
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

