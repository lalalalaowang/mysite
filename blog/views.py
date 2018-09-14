from django.shortcuts import render, get_object_or_404
from .models import Blog, BlogType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def blog_list(request):
    blog_types = BlogType.objects.all()
    object_list = Blog.published.all()
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)
    return render(request, 'blog/blog_list.html',
     {'page':page, 'blogs':blogs ,'blog_types':blog_types})

def blog_detail(request, year, month, day, blog_slug):
    blog = get_object_or_404(Blog,
        status='published',
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=blog_slug)
    return render(request, 'blog/blog_detail.html', {'blog':blog})
