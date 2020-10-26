from django.urls import path
from .views import (
    IndexView,
    PostDetailView,
    PostCreateView,
    SearchPostView
)

app_name = 'blog'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='postdetail'),
    path('post/create/', PostCreateView.as_view(), name='postcreate'),
    path('search/', SearchPostView.as_view(), name='search_post'),
]
