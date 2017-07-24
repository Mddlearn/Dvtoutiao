# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
from bs4 import BeautifulSoup
import requests
from django.contrib.auth.models import AbstractUser


class NewUser(AbstractUser):
    nick_name = models.CharField(max_length=50)
    head_image = models.ImageField(upload_to='photos')
    descriptions = models.CharField(max_length=200, blank=True)

    def __unicode__(self):
        return self.username

    def is_following(self, user):
        return self.newuser_follower.filter(followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        return self.newuser_followed.filter(follower_id=user.id).first() is not None

    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            f.save()

    def unfollow(self, user):
        f = self.newuser_follower.filter(followed_id=user.id).first()
        if f:
            f.delete()


class PublicSignal(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(NewUser)
    created_time = models.DateTimeField(auto_now_add=True)
    head_image = models.ImageField(upload_to='photos')
    desc = models.CharField(max_length=200, blank=True)

    def __unicode__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField(max_length=100)
    public_signal = models.ForeignKey(PublicSignal)
    created_time = models.DateTimeField(auto_now_add=True)
    short_url = models.CharField(max_length=50, blank=True)
    creator = models.ForeignKey(NewUser)
    tags = models.ManyToManyField(Tag)
    collections = models.ForeignKey('Collection', blank=True)
    summary = models.TextField(blank=True)

    class Mate:
        ordering = ['-created_time']

    def __unicode__(self):
        return self.title

    @staticmethod
    def get_summary(url):
        r = requests.get(url)
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, 'lxml')
        tags = soup.find_all('p')
        content = ''
        for tag in tags[:10]:
            for string in tag.stripped_strings:
                if string:
                    content = content + string
        return content

    def save(self, *args, **kwargs):
        if not self.short_url:
            self.short_url = (re.search(
                'https://(.+?)/.*', self.url)).group(1)
        if not self.summary:
            self.summary = self.get_summary(self.url)
        super(Article, self).save(*args, **kwargs)


class Comment(models.Model):
    body = models.TextField()
    creator = models.ForeignKey(NewUser)
    created_time = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article)

    def __unicode__(self):
        return self.body


class Poll(models.Model):
    user = models.ForeignKey(NewUser)
    article = models.ForeignKey(Article)

    def __unicode__(self):
        return self.user.username


class Collection(models.Model):
    name = models.CharField(max_length=100, default='Collection')
    user = models.ForeignKey(NewUser)

    def __unicode__(self):
        return self.name


class Pollarticle(models.Model):
    poll_article = models.ForeignKey(Article)
    polls = models.IntegerField(default=0)

    def __unicode__(self):
        return self.poll_article.title


class Follow(models.Model):
    follower = models.ForeignKey(NewUser, related_name='newuser_follower')
    followed = models.ForeignKey(NewUser, related_name='newuser_followed')
    timestamp = models.DateTimeField(auto_now_add=True)
