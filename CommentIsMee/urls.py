from django.conf.urls import url, include

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^', include('articles.urls', namespace="articles")),
    url(r'^admin/', include(admin.site.urls)),
]