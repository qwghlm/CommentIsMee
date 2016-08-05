from django.conf.urls import url

from articles import views

urlpatterns = [
    url(r'^$', views.index, name='Home'),
	url(r'^(?P<article_id>\d+)/$', views.detail, name='detail'),
]

