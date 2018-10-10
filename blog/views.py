from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required


def index(request):
    selected = 'index'
    return render(request, 'index.html', {'selected': selected})


@login_required
def post_list(request):
    object_list = Post.objects.all()
    paginator = Paginator(object_list, 10)
    page = request.GET.get('page', 1)
    try:
        posts = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        posts = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        posts = paginator.page(page)
    selected = 'post_list'
    page_nums = [str(i) for i in range(1, paginator.num_pages+1)]
    return render(request, 'blog/post_list.html', {'posts': posts, 'page': page,
                                                   'page_nums': page_nums, 'selected': selected})


def post_detail(request, year, month, day, post_slug):
    post = get_object_or_404(Post, slug=post_slug,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,
                             status='published')
    selected = 'post_list'
    return render(request, 'blog/post_detail.html', {'post': post, 'selected': selected})
