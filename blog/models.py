from django.db import models

NULLABLE = {"blank": True, "null": True}


class BlogPost(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name="Заголовок")
    body = models.TextField(verbose_name="Содержимое статьи", **NULLABLE)
    preview = models.ImageField(
        upload_to="blog/%Y/%m", verbose_name="Изображение", **NULLABLE
    )
    date_published = models.DateField(auto_now_add=True, verbose_name="Дата публикации")
    count_views = models.IntegerField(default=0, verbose_name="Количество просмотров")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Запись в блоге"
        verbose_name_plural = "Записи в блоге"
        ordering = ["date_published"]
