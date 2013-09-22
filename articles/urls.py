from django.conf.urls import patterns, url

from articles import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='Home'),
    url(r'^add/$', views.add, name='Add'),
	url(r'^(?P<article_id>\d+)/$', views.detail, name='detail'),
)

