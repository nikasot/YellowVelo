# Generated by Django 4.0.3 on 2022-05-11 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'get_latest_by': 'name', 'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='cycle',
            options={'get_latest_by': 'slug', 'verbose_name': 'Велосипед', 'verbose_name_plural': 'Велосипеды'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'get_latest_by': 'email', 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата Регистрации'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, verbose_name='Права администратора'),
        ),
    ]
