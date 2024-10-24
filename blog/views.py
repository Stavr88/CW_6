from django.urls import reverse_lazy
from django.urls.base import reverse
from django.views.generic import (
    DetailView,
    CreateView,
    ListView,
    UpdateView,
    DeleteView,
)

from blog.models import BlogPost
from blog.services import get_posts_from_cache


class PostCreateView(CreateView):
    model = BlogPost
    fields = ["title", "body", "preview"]
    success_url = reverse_lazy("blog:view_list")


class PostListView(ListView):
    model = BlogPost
    ordering = ["date_published"]

    def get_queryset(self):
        return get_posts_from_cache()


class PostDetailView(DetailView):
    model = BlogPost

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.count_views += 1
        self.object.save()
        return self.object


class PostUpdateView(UpdateView):
    model = BlogPost
    fields = ["title", "body", "preview"]

    def get_success_url(self):
        return reverse("blog:view_post", args=[self.kwargs.get("pk")])


class PostDeleteView(DeleteView):
    model = BlogPost
    success_url = reverse_lazy("blog:view_list")
