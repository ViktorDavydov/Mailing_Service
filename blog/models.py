from django.db import models
from django.urls import reverse

NULLABLE = {'null': True, 'blank': True}


class Blog(models.Model):
    article_name = models.CharField(max_length=30, verbose_name='заголовок')
    slug = models.CharField(max_length=150, verbose_name='slug', **NULLABLE)
    contents = models.TextField(verbose_name='содержимое')
    publication_date = models.DateField(auto_now=False, auto_now_add=False,
                                        verbose_name='дата публикации')
    views_count = models.IntegerField(default=0, verbose_name='количество просмотров')
    is_published = models.BooleanField(default=True, verbose_name="опубликовано")

    def __str__(self):
        return f'{self.article_name} - {self.slug}'

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'
        ordering = ('article_name',)

    def get_absolute_url(self):
        return reverse('blog', kwargs={'post_slug': self.slug})
