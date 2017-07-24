from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^subjects/(?P<pk>[0-9]$)',
        views.publicSignal, name='publicSignal'),
    url(r'^user/(?P<pk>[0-9]+)/info$', views.user_info, name='userinfo'),
    url(r'^post/(?P<pk>[0-9]+)$', views.article_detail, name='article_detail'),
    url(r'^login$', views.login_in, name='login'),
    url(r'^logout$', views.log_out, name='logout'),
    url(r'^explore$', views.public_signal_number, name='psnumber'),
    url(r'^poll/(?P<pk>[0-9]+)$', views.get_pull_article, name='poll'),
    url(r'^collection/(?P<pk>[0-9]+)$',
        views.get_collection_article, name='collection'),
    url(r'^user/(?P<pk>[0-9]+)/colls$', views.user_collection, name='colls'),
    url('^posts/popular', views.popular_sharing, name='popularsharing'),
    url(r'user/(?P<pk>[0-9]+)/subjects$',
        views.user_collection_number, name='user_coll_number'),
    url(r'^user/(?P<pk>[0-9]+)/info/follow$', views.follow, name='follow'),
    url(r'^user/(?P<pk>[0-9]+)/info/unfollow$',
        views.unfollow, name='unfollow'),
    url(r'^user/(?P<pk>[0-9]+)/info/followed$',
        views.followed, name='followed'),
    url(r'^user/(?P<pk>[0-9]+)/info/follower$',
        views.follower, name='follower'),

]
