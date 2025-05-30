# Generated by Django 5.2 on 2025-05-04 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, verbose_name='Название')),
                ('price', models.FloatField(verbose_name='Цена')),
                ('image', models.ImageField(blank=True, max_length=230, null=True, upload_to='product_images/', verbose_name='Фотография')),
                ('thumbnail', models.ImageField(blank=True, max_length=230, null=True, upload_to='product_images/', verbose_name='Фотография')),
                ('tags', models.CharField(max_length=300, verbose_name='Теги')),
            ],
            options={
                'verbose_name': 'Букет',
                'verbose_name_plural': 'Букеты',
            },
        ),
    ]
