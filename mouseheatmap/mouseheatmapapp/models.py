import datetime
from turtle import update
from django.db import models
from django.utils import timezone
from django.contrib import admin

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    
    def __str__(self):
        return self.question_text

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

class InitialData(models.Model):
    folder_path = models.CharField(max_length=255,default='')
    min_duration_time = models.IntegerField(default=0)
    max_duration_time = models.IntegerField(default=0)
    min_mouse_movement = models.IntegerField(default=0)
    max_mouse_movement = models.IntegerField(default=0)
    min_mouse_click = models.IntegerField(default=0)
    max_mouse_click = models.IntegerField(default=0)
    pub_date = models.DateTimeField(auto_now=True)