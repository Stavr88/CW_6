from django.core.cache import cache

from blog.models import BlogPost
from config.settings import CACHE_ENABLED


def get_posts_from_cache():
    if not CACHE_ENABLED:
        return BlogPost.objects.all()
    posts = cache.get("posts_list")
    if posts is not None:
        return posts
    posts = BlogPost.objects.all()
    cache.set("posts_list", posts)
    return posts
