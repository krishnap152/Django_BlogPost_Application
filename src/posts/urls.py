from django.contrib import admin
from django.urls import path,re_path
from .views import (post_list,post_create,post_detail,post_update,post_delete)

app_name="posts"
urlpatterns = [
    path('', post_list, name="list"),
    path('create/', post_create),
    path('<str:slug>/', post_detail,name="detail"),
    path('<str:slug>/edit/', post_update, name='update'),
    path('<str:slug>/delete/', post_delete),
]
