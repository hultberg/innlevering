from django.conf.urls import patterns, include, url

from . import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ppinnlevering.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^view/(?P<composlug>[0-9]+)/upload/handle/', views.uploadhandler, name='upload_handle'),
    url(r'^view/(?P<composlug>[0-9]+)/upload/$', views.uploadview, name='upload'),
    url(r'^view/(?P<composlug>[0-9]+)/$', views.compoview, name='view_compo'),
    url(r'^login/', views.loginview, name='loginview'),
    url(r'^register/', views.registerview, name='registerview'),
    url(r'^logout/', views.logouthandle, name='logoutview'),
    url(r'^$', views.indexview, name='index'),
)
