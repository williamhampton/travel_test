from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'^add$', views.add),
    url(r'^login$',views.login),
    url(r'^travels$', views.locations),
    url(r'^travels/add', views.adddestination),
    url(r'^newdestination', views.newdestination),
    url(r'^travels/destination/(?P<id>\d+)$', views.viewdestination),
    url(r'^join/(?P<id>\d+)$', views.join ),
]
