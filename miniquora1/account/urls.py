from django.conf.urls import url,include

from . import views

urlpatterns = [
        url(r'^logout/$','account.views.logout',name = 'logout'),
        url(r'^home/$','account.views.home', name = 'home'),
        url(r'^signup/$','account.views.signup', name = 'signup'),
        url(r'^activate/(?P<uid>\d+)/(?P<token>[0-9A-Za-z_\-]+)/$', 'account.views.activate', name='activate'),
        url(r'^reset_password/(?P<uid>\d+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'account.views.reset_password', name = 'reset_password'),
        url(r'^forgot_password/$', 'account.views.forgot_password', name = 'forgot_password'),
    ]
