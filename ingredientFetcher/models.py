# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Ingredients (models.Model):
    dish = models.CharField(max_length=20,null=True);
    ingredients = models.CharField(max_length=2000,null=True);

    def __str__(self):
        return self.dish;

class UserActivity (models.Model):
    userId = models.CharField(max_length=30,null=False)
    topic = models.CharField(max_length=20,null=False)
    lastActive = models.DateField(null=True)
    context = models.IntegerField(null=True)


    def __str__(self):
        return self.userId;