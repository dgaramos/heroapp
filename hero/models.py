# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Hero(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100, choices=(('M', 'Male'), ('F', 'Female')), default='F')
    mainTeam = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class SuperHeroTeam(models.Model):
    name = models.CharField(max_length=100)
    heroes = models.ManyToManyField(Hero)
    editor = models.CharField(max_length=100, choices=(('Marvel', 'Marvel'), ('DC', 'Detective Comics')), default='Marvel')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
