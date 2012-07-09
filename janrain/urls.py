from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('janrain.views',
    url(r'^login/$', 'login', name='janrain_login'),
    url(r'^logout/$', 'logout', name='janrain_logout'),
)
