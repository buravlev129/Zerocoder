from django.db import models


class Film(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название фильма")
    description = models.TextField(verbose_name="Краткое описание фильма")
    review = models.TextField(verbose_name="Отзыв о фильме")
    image = models.ImageField(upload_to='films/img/', verbose_name="Изображение", blank=True, null=True)
 
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"

