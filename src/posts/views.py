from django.contrib import messages
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
import urllib.parse as parse


from .forms import PostForm
from .models import Post

# Create your views here.

def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form = PostForm(request.POST or None, request.FILES or None)
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


def post_detail(request,slug=None):
    instance = get_object_or_404(Post,slug=slug)
    share_string = parse.quote(instance.content)
    context = {
        "title":instance.title,
        "instance":instance,
        "share_string":share_string,
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

	queryset_list = Post.objects.all() #.order_by("-timestamp")
	paginator = Paginator(queryset_list, 10) # Show 25 contacts per page
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
		"page_request_var": page_request_var
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
