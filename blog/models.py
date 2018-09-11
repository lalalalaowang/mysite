from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User


class BlogType(models.Model):
    
    type_name = models.CharField(max_length=20)

    def __str__(self):
        return self.type_name


class PublishedManager(models.Manager):
    
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset()\
        .filter(status='published')


class Blog(models.Model):
    
    STATUS_CHOICES = (
        ('draft','Draft'),
        ('published','Published'),
    )
    title = models.CharField(max_length=30)
    slug = models.SlugField(max_length=250,
        unique_for_date='publish')
    content = models.TextField()
    author = models.ForeignKey(User, 
        on_delete=models.CASCADE,
        related_name='blog_blogs')
    publish = models.DateTimeField(default=timezone.now)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
        choices=STATUS_CHOICES,
        default='draft')
    blog_type = models.ForeignKey(BlogType, 
        on_delete=models.CASCADE)

    objects = models.Manager()

    published = PublishedManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:blog_detail',
            args=[self.publish.year,
                  self.publish.month,
                  self.publish.day,
                  self.slug,])
