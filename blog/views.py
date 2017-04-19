from django.shortcuts import render

# Create your views here.
from .models import Article
from .form import ArticleForm
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
import os
from django.http import HttpResponse
import time
import json

def post_detail(request, pk):
    post = get_object_or_404(Article, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


# Create your views here.
def post_list(request):
    posts = Article.objects.filter(published_date__isnull=False).order_by('-published_date')
    for p in posts:
        print(p.published_date)
        print(p.text)
        break
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_new(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = ArticleForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_draft_list(request):
    posts = Article.objects.filter(published_date__isnull=True).order_by('-created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

def post_publish(request, pk):
    post = get_object_or_404(Article, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

def post_edit(request, pk):
    post = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = ArticleForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def post_remove(request, pk):
    post = get_object_or_404(Article, pk=pk)
    post.delete()
    return redirect('../../..')

def mkdir(path):                                         #路径初始化，如果没有存放地点就新建
      path = path.strip()
      path = path.rstrip("\\")
      if not os.path.exists(path):
          os.makedirs(path)
      return path

def save_file(path, file_name, data):                   #把data保存path/file_name文件中
      if data == None:
          return
      mkdir(path)
      if(not path.endswith("/")):
          path=path+"/"
      file = open(path+file_name,"wb")
      file.write(data)
      file.flush()
      file.close()

def uploadImg(request):
     if request.method=='POST':
         #file_obj = open("log.txt","w+")
         buf = request.FILES.get('imgFile',None)                                    #获取的图片文件
         print(request.FILES.keys())
         print("_______________")
         #print >> file_obj, str(buf)
         file_buff = buf.read()                                                  #获取图片内容
         time_format=str(time.strftime("%Y-%m-%d-%H%M%S",time.localtime()))
         file_name = "img"+time_format+".jpg"                                    #img2016-02-13-072459.jpg
         save_file("blog/static/image", file_name,file_buff)                     #blog/static/image/img2016-02-13-072459.jpg
         dict_tmp = {}                                                           #kindeditor定义了返回的方式是json，
         dict_tmp['error']=0                                                     #成功{ "error":0, "url": "/static/image/filename"}
         dict_tmp['url']="/static/image/"+file_name
         return HttpResponse(json.dumps(dict_tmp))