from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from unidecode import unidecode
from django.shortcuts import reverse
from django.utils.text import slugify


# Create your models here.


class Cycle(models.Model):
    title = models.CharField('Название', max_length=50)
    slug = models.SlugField('URL товара', max_length=50, unique=True, db_index=True)
    description = models.TextField('Описание')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')
    image = models.ImageField('Картинка', upload_to='shop')
    price = models.IntegerField('Цена')

    class Meta:
        verbose_name = 'Велосипед'  # Заменяем имя на нужное в названии Модели
        verbose_name_plural = 'Велосипеды'  # Замена множественного числа
        get_latest_by = 'slug'

    def get_absolute_url(self):
        return reverse('shop:show_cycle', kwargs={'cycle_slug': self.slug})

    def save(self, *args, **kwargs):
        last_obj = Cycle.objects.all().order_by('id').last()
        if last_obj:
            last_pk = last_obj.pk + 1
        else:
            last_pk = 1
        string = unidecode(str(self.title) + str(last_pk))
        self.slug = slugify(string)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField('Название категории', max_length=20, unique=True, db_index=True)
    slug = models.SlugField('URL', max_length=20, unique=True, db_index=True)
    image = models.ImageField('Картинка', upload_to='shop')

    class Meta:
        verbose_name = 'Категория'  # Заменяем имя на нужное в названии Модели
        verbose_name_plural = 'Категории'  # Замена множественного числа
        get_latest_by = 'name'

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        # if not username:
        #     raise ValueError('Задайте Имя')
        if not email:
            raise ValueError('Задайте почтовый адрес')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields['is_staff'] = False
        extra_fields['is_superuser'] = False
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Почтовый адрес', max_length=50, db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField('Права администратора', default=False)
    date_joined = models.DateTimeField('Дата Регистрации',auto_now_add=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'  # Заменяем имя на нужное в названии Модели
        verbose_name_plural = 'Пользователи'  # Замена множественного числа
        get_latest_by = 'email'
    # @classmethod
    # def get_username_by_id(cls, id):
    #     user = cls.objects.get(pk=id)
    #     username = user.email.split("@")[0]
    #     return username
    #
    # print(get_username_by_id(1))
