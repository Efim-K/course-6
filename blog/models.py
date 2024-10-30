from django.db import models
from django.utils.text import slugify

NULLABLE = {"blank": "True", "null": "True"}


# Create your models here.
class Blog(models.Model):
    """
    Блог с опубликованными статьями и превью изображений.
    """
    # заголовок;
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    # slug строка идентификатор, понятная человеку (в отличие от ID) и содержащая только "безопасные" символы:
    # - 0-9
    # - a-z (общепринято - в нижнем регистре)
    # - символ -
    # - иногда еще символ _
    slug = models.CharField(max_length=200, verbose_name='slug', **NULLABLE)
    # content;
    content = models.TextField(verbose_name='Содержимое')
    # превью(изображение);
    preview = models.ImageField(upload_to="blog", verbose_name='Превью', **NULLABLE)
    # дата создания;
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    # признак публикации;
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    # количество просмотров;
    views_count = models.IntegerField(default=0, verbose_name='Количество просмотров')

    def save(self, *args, **kwargs):
        """
        Создаёт slug и сохраняет публикацию
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        """
        Meta-данные модели.
        """
        verbose_name = "блог"
        verbose_name_plural = "блоги"
        ordering = (
            "title",
        )
