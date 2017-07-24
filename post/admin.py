# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Article, NewUser, PublicSignal, Tag, Comment, Collection, Poll, Pollarticle, Follow


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'created_time', 'collections', 'summary')


class NewUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'nick_name',
                    'descriptions', 'head_image', 'password', 'is_active')


class PublicSignalAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'created_time', 'head_image')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('body', 'creator', 'created_time')


class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')


class PollAdmin(admin.ModelAdmin):
    list_display = ('user', 'article')


class PollarticleAdmin(admin.ModelAdmin):
    list_display = ('poll_article', 'polls')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'followed', 'timestamp')


admin.site.register(Article, ArticleAdmin)
admin.site.register(NewUser, NewUserAdmin)
admin.site.register(PublicSignal, PublicSignalAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Poll, PollAdmin)
admin.site.register(Pollarticle, PollarticleAdmin)
admin.site.register(Follow, FollowAdmin)
