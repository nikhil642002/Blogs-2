from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
from .form import PostForm
# Create your views here.
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form" : form
    }
    return render(request, "post_form.html", context)

def post_detail(request, id=None):
    instance = Post.objects.get(id=id)
    context = {
        "title" : instance.title,
        "instance" : instance
    }
    return render(request, "post_detail.html", context)

def post_list(request):
    queryset_list = Post.objects.all()
    paginator = Paginator(queryset_list, 10)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    context = {
        "title" : 'list',
        'object_list' : queryset,
        'page_request_var':page_request_var
    }
    return render(request, "post_list.html", context)

def post_update(request, id=None):
    instance = Post.objects.get(id=id)
    form = PostForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully Updated")
        return HttpResponseRedirect(instance.get_absolute_url())
   # else:
    #    messages.error(request, "Not Successfully Updated")
    context = {
        "title" : instance.title,
        "instance" : instance,
        "form" : form
    }
    return render(request, "post_form.html", context)

def post_delete(request, id = None):
    instance = Post.objects.get(id=id)
    instance.delete()
    messages.success(request, "Successfully Deleted")
    return redirect("posts:list")