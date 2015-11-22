"""
  Copyright 2015 Edvin Hultberg

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
"""

from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
    url(r'^view/(?P<composlug>[0-9]+)/upload/handle/', views.uploadhandler, name='upload_handle'),
    url(r'^view/(?P<composlug>[0-9]+)/upload/$', views.uploadview, name='upload'),
    url(r'^view/(?P<composlug>[0-9]+)/$', views.compoview, name='view_compo'),
    url(r'^view/(?P<composlug>[0-9]+)/bidrags/$', views.compobidragview, name='viewbidrag'),
    url(r'^view/(?P<composlug>[0-9]+)/b/(?P<bidragslug>[0-9]+)/$', views.composinglebidragview, name='viewsinglebidrag'),
    url(r'^view/(?P<composlug>[0-9]+)/b/(?P<bidragslug>[0-9]+)/delete/$', views.bidragdelete, name='bidragdelete'),
    url(r'^view/(?P<composlug>[0-9]+)/b/(?P<bidragslug>[0-9]+)/save/$', views.bidrageditsave, name='bidrageditsave'),
    url(r'^view/(?P<composlug>[0-9]+)/b/(?P<bidragslug>[0-9]+)/vote/$', views.bidragvote, name='bidragvote'),
    #url(r'^view/(?P<composlug>[0-9]+)/b/(?P<composlug>[0-9]+)/$', views.bidragview, name='view_bidrag'),
    url(r'^account/login/', views.loginview, name='loginview'),
    url(r'^account/logout/', views.logouthandle, name='logoutview'),
    url(r'^account/view/', views.accountview, name='accountview'),
    url(r'^account/bidrags/', views.mybidrags, name='mybidrags'),
    url(r'^$', views.indexview, name='index'),
)
