from django.conf.urls import url,include

from . import views

urlpatterns = [
        url(r'^login/$','account.views.login',name = 'login'),
        url(r'^logout/$','account.views.logout',name = 'logout'),
        url(r'^secret/$','account.views.secret', name = 'secret')
    ]
