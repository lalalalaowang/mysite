from django.urls import path
from . import views

app_name = 'blog'

urlpatterns =[
    path('', views.index, name='index'),
    path('post_list/', views.post_list, name='post_list'),
    path('post_detail/<int:year>/<int:month>/<int:day>/<slug:post_slug>', views.post_detail, name='post_detail'),
]