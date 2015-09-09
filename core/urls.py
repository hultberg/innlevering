from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
    url(r'^view/(?P<composlug>[0-9]+)/upload/handle/', views.uploadhandler, name='upload_handle'),
    url(r'^view/(?P<composlug>[0-9]+)/upload/$', views.uploadview, name='upload'),
    url(r'^view/(?P<composlug>[0-9]+)/$', views.compoview, name='view_compo'),
    url(r'^view/(?P<composlug>[0-9]+)/bidrags/$', views.compobidragview, name='viewbidrag'),
    url(r'^view/(?P<composlug>[0-9]+)/b/(?P<bidragslug>[0-9]+)$', views.composinglebidragview, name='viewsinglebidrag'),
    #url(r'^view/(?P<composlug>[0-9]+)/b/(?P<composlug>[0-9]+)/$', views.bidragview, name='view_bidrag'),
    url(r'^account/login/', views.loginview, name='loginview'),
    url(r'^account/register/', views.registerview, name='registerview'),
    url(r'^account/logout/', views.logouthandle, name='logoutview'),
    url(r'^account/view/', views.accountview, name='accountview'),
    url(r'^$', views.indexview, name='index'),
)
