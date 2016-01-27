from django.conf.urls import url,include

from . import views

urlpatterns = [
        url(r'^logout/$','account.views.logout',name = 'logout'),
        url(r'^home/$','account.views.home', name = 'home'),
        url(r'^signup/$','account.views.signup', name = 'signup'),
        url(r'^activate/(?P<uid>\d+)/(?P<token>[0-9A-Za-z_\-]+)/$', 'account.views.activate', name='activate')
    ]
