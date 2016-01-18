from django.conf.urls import url,include

from . import views

urlpatterns = [
        url(r'^logout/$','account.views.logout',name = 'logout'),
        url(r'^home/$','account.views.home', name = 'home')
    ]
