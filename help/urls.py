from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ppinnlevering.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^help/$', views.helpindex, name='helpindex'),
)
