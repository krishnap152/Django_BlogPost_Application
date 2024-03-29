#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 14:42:48 2019

@author: krishna
"""

from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
import urllib.parse as parse
from django.db.models import Q
from django.utils import timezone

from .forms import PostForm
from .models import Post

# Create your views here.


def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    if not request.user.is_authenticated:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        # print(form.cleaned_data.get("title"))
        instance.user = request.user
        instance.save()
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    # if request.method == "POST":
    #     print(request.POST.get("content"))
    #     print(request.POST.get("title"))
    #     title = request.POST.get("title")
    #     Post.objects.creat(title=title)
    context = {
        "form": form,
    }
    # return HttpResponse("<h1>create</h1>")
    return render(request, "post_form.html", context)


def post_detail(request, slug=None):
    instance = get_object_or_404(Post, slug=slug)
    if instance.draft or instance.publish > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = parse.quote(instance.content)
    context = {
        "title": instance.title,
        "instance": instance,
        "share_string": share_string,
    }
    return render(request, "post_detail.html", context)


def post_list(request):
    # return HttpResponse("<h1>list</h1>")
    # if request.user.is_authenticated:
    #     context = {
    #         "title":"User is authenticated"
    #     }
    # else:
    #     context = {
    #         "title":"User is Not authenticated"
    #     }
    today = timezone.now()
    queryset_list = Post.objects.active()
    # .order_by("-timestamp")
    # queryset_list = Post.objects.filter(draft=False).filter(publish__lte=timezone.now()) #.order_by("-timestamp")
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()
    
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
            Q(title__icontains=query) |
            Q(content__icontains = query) |
            Q(user__first_name__icontains = query) |
            Q(user__last_name__icontains = query)
            ).distinct()
    paginator = Paginator(queryset_list, 10)
    # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    context = {
		"object_list": queryset, 
		"title": "List",
		"page_request_var": page_request_var,
        "today":today
	}
    return render(request, "post_list.html", context)


def post_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
		"title": instance.title,
		"instance": instance,
		"form":form,
	}
    return render(request, "post_form.html", context)

def post_delete(request,slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    instance = get_object_or_404(Post,slug=slug)
    instance.delete()
    messages.success(request,"Successfully deleted")
    return redirect("posts:list")
