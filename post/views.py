# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Article, PublicSignal, NewUser, Comment, Tag, Poll, Collection, Pollarticle, Follow
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import urlparse


def index(request):
    article_list = Article.objects.all()
    context = {'article_list': article_list}
    return render(request, 'index.html', context)


def publicSignal(request, pk):
    public_article_list = Article.objects.filter(public_signal_id=pk)
    public_signal = PublicSignal.objects.get(id=pk)
    context = {'public_article_list': public_article_list,
               'public_signal': public_signal}
    return render(request, 'publicsignal.html', context)


def user_info(request, pk):
    user_article_list = Article.objects.filter(creator_id=pk)
    creator = NewUser.objects.get(id=pk)
    collection = Collection.objects.filter(user=creator).first()
    collection_article_list = Article.objects.filter(collections=collection)
    context = {'user_article_list': user_article_list, 'creator': creator,
               'collection_article_list': collection_article_list}
    return render(request, 'userinfo.html', context)


def article_detail(request, pk):
    article = Article.objects.get(id=pk)
    comments = Comment.objects.filter(article_id=pk)
    tags = Tag.objects.filter(article=pk)
    context = {'article': article, 'comments': comments, 'tags': tags}
    return render(request, 'article_detail.html', context)


def login_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                messages.success(request, u'成功登录')
                return redirect('/')
            else:
                messages.error(request, u'密码或用户名错误')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


@login_required
def log_out(request):
    logout(request)
    messages.success(request, u'已注销')
    return redirect('/')


def public_signal_number(request):
    public_signal_list = PublicSignal.objects.all()
    context = {'public_signal_list': public_signal_list}
    return render(request, 'exclusivenumber.html', context)


@login_required
def get_pull_article(request, pk):
    logged_user = request.user
    article = Article.objects.get(id=pk)
    polls = logged_user.poll_set.all()
    articles = []
    for poll in polls:
        articles.append(poll.article)
    if article in articles:
        url = urlparse.urljoin('/post/', pk)
        return redirect(url)
    else:
        poll = Poll(user=logged_user, article=article)
        poll.save()
        return redirect('/')


@login_required
def get_collection_article(request, pk):
    logged_user = request.user
    collection = Collection.objects.get(user=logged_user)
    if collection is None:
        coll = Collection(user=logged_user)
        coll.save()
    else:
        article = Article.objects.get(id=pk)
        articles = collection.article_set.all()
        if article in articles:
            url = urlparse.urljoin('/post/', pk)
            return redirect(url)
        else:
            article.collections = collection
            article.save()
        return redirect('/')


def user_collection(request, pk):
    creator = NewUser.objects.get(id=pk)
    collection = Collection.objects.get(user=creator.id)
    collection_article_list = Article.objects.filter(collections=collection)
    context = {'collection_article_list': collection_article_list,
               'creator': creator}
    return render(request, 'usercoll.html', context)


def popular_sharing(request):
    articles = Article.objects.all()
    for article in articles:
        if article:
            polls = article.poll_set.all().count()
            poll_list = Pollarticle(poll_article=article, polls=polls)
            if not Pollarticle.objects.filter(poll_article=article).first():
                poll_list.save()
            else:
                pass
    popular_sharing_list = Pollarticle.objects.order_by('-polls')
    context = {'popular_sharing_list': popular_sharing_list}
    return render(request, 'popularsharingarticle.html', context)


def user_collection_number(request, pk):
    creator = NewUser.objects.get(id=pk)
    collections = PublicSignal.objects.filter(creator=creator)
    context = {'creator': creator, 'collections': collections}
    return render(request, 'usernumber.html', context)


@login_required
def follow(request, pk):
    user = NewUser.objects.filter(id=pk).first()
    if user is None:
        messages.error(request, u'没有此用户')
        return redirect('/')
    if request.user.is_following(user):
        messages.success(request, u'您已关注此用户')
        return redirect('userinfo', pk=user.id)
    request.user.follow(user)
    messages.success(request, u'你正在关注该用户')
    return redirect('/user/1/info')


@login_required
def unfollow(request, pk):
    user = NewUser.objects.filter(id=pk).first()
    if user is None:
        messages.error(request, u'没有该用户')
        return redirect('/')
    if not request.user.is_following(user):
        messages.success(request, u'还未关注此用户')
        return redirect('userinfo', pk=user.id)
    request.user.unfollow(user)
    messages.success(request, u'你正在取消关注该用户')
    return redirect('userinfo', pk=user.id)


def followed(request, pk):
    creator = NewUser.objects.get(id=pk)
    followeds = Follow.objects.filter(follower_id=creator.id).all()
    context = {'followeds': followeds, 'creator': creator}
    return render(request, 'userfollowed.html', context)


def follower(request, pk):
    creator = NewUser.objects.get(id=pk)
    followers = Follow.objects.filter(followed_id=creator.id).all()
    context = {'creator': creator, 'followers': followers}
    return render(request, 'userfollower.html', context)
