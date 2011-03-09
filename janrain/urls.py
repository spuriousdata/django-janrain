from django.conf.urls.defaults import *

urlpatterns = patterns('janrain.views',
    (r'^login/$', 'login'),
    (r'^logout/$', 'logout'),
    (r'^loginpage/$', 'loginpage'),
)
