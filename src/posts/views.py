from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect

from .forms import PostForm
from .models import Post

# Create your views here.

def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        #print(form.cleaned_data.get("title"))
        instance.save()
        messages.success(request,"Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    # if request.method == "POST":
    #     print(request.POST.get("content"))
    #     print(request.POST.get("title"))
    #     title = request.POST.get("title")
    #     Post.objects.creat(title=title)
    context = {
        "form":form,
    }
    #return HttpResponse("<h1>create</h1>")
    return render(request,"post_form.html",context)


def post_detail(request,id):
    instance = get_object_or_404(Post,id=id)
    context = {
        "title":"detail",
        "instance":instance
    }
    return render(request,"post_detail.html",context)

def post_list(request):
    #return HttpResponse("<h1>list</h1>")
    #if request.user.is_authenticated:
     #   context = {
      #      "title":"User is authenticated"
       # }
   # else:
    #    context = {
     #       "title":"User is Not authenticated"
      #  }

    queryset = Post.objects.all()
    context = {
        "object_list":queryset,
        "title":"queryset"
    }
    return render(request,"post_list.html",context)

def post_update(request,id=None):
    instance = get_object_or_404(Post,id=id)
    form = PostForm(request.POST or None,instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
        messages.SUCCESS(request,"Saved")
    context = {
        "title": instance.title,
        "instance" : instance,
        "form":form
    }
    return render(request,"post_form.html",context)

def post_delete(request,id=None):
    instance = get_object_or_404(Post,id=id)
    instance.delete()
    messages.success(request,"Successfully deleted")
    return redirect("posts:list")