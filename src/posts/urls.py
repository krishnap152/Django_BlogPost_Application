from django.contrib import admin
from django.urls import path,re_path
from .views import (post_list,post_create,post_detail,post_update,post_delete)

app_name="posts"
urlpatterns = [
    path('', post_list, name="list"),
    path('create/', post_create),
    re_path(r'^(?P<id>\d+)/$', post_detail,name="detail"),
    re_path(r'^(?P<id>\d+)/edit/$', post_update, name='update'),
    re_path(r'^(?P<id>\d+)/delete/', post_delete),
]
