from django.urls import path

from blog.apps import BlogConfig
from blog.views import (
    PostCreateView,
    PostListView,
    PostDetailView,
    PostUpdateView,
    PostDeleteView,
)

app_name = BlogConfig.name

urlpatterns = [
    path("create/", PostCreateView.as_view(), name="create_post"),
    path("", PostListView.as_view(), name="view_list"),
    path("view/<int:pk>/", PostDetailView.as_view(), name="view_post"),
    path("edit/<int:pk>/", PostUpdateView.as_view(), name="edit_post"),
    path("delete/<int:pk>/", PostDeleteView.as_view(), name="delete_post"),
]
