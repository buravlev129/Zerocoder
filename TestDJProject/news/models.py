from django.core.exceptions import ValidationError
from django.db import models


def validate_positive(value):
    if value <= 0:
        raise ValidationError('Значение должно быть больше нуля.')

class NewsPost(models.Model):
    title = models.CharField("Заголовок новости", max_length=200)
    short_description = models.CharField("Краткое описание новости", max_length=200)
    text = models.TextField("Новость")
    pub_date = models.DateTimeField("Дата публикации")
    username = models.CharField("Имя пользователя", default="", max_length=100)

    image = models.ImageField(upload_to='news_images/', verbose_name="Изображение", blank=True, null=True)
    image_width = models.PositiveIntegerField("Ширина картинки", default=0, validators=[validate_positive], blank=True, null=True)
    image_height = models.PositiveIntegerField("Высота картинки", default=0, validators=[validate_positive], blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.image and not self.image_width and not self.image_height:
            # Если изображение загружено, но ширина и высота не указаны, автоматически заполняем их
            from PIL import Image
            img = Image.open(self.image)
            self.image_width, self.image_height = img.size
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.image and (not self.image_width or not self.image_height):
            raise ValidationError('Ширина и высота изображения должны быть указаны, если загружено изображение.')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

