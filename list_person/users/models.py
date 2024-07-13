from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from PIL import Image
from .data_field import WORKING_POSITION, FILIAL, DEPARTMENT
from django.utils import timezone
from django.utils.text import slugify


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField('ФИО', default='Иванов Иван', max_length=100)
    slug = models.SlugField(verbose_name='URL', max_length=255, blank=True, unique=True)
    images = models.ImageField('Фото профиля', default='default.jpg', upload_to='user_images')
    date = models.DateField('Дата вступление на работу', default=timezone.now)
    account_type = models.CharField('Должность', choices=WORKING_POSITION, default='Employee', max_length=20)
    filial = models.CharField('Филиал', choices=FILIAL, default='Moscow', max_length=20)
    department = models.CharField('Отделение', choices=DEPARTMENT, default='Developers', max_length=20)
    salary = models.IntegerField('Оклад', default=50000)

    def __str__(self):
        return f'Данные коллеги {self.user.username}'

    def get_absolute_url(self):
        return reverse('profile-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super().save()

        image = Image.open(self.images.path)

        if image.height > 256 or image.width > 256:
            resize = (256, 256)
            image.thumbnail(resize)
            image.save(self.images.path)

