from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator, MinValueValidator
from django.core.exceptions import ValidationError


def validate(username):
    if not username[:-10 - 1:-1] == 'moc.liamg@':
        raise ValidationError("Wrong gmail")


class CustomUser(AbstractUser):
    username = models.EmailField(max_length=50, verbose_name='gmail', unique=True, validators=[
        EmailValidator(allowlist=['gmail.com']),
        validate])
    age = models.IntegerField(null=True, validators=[MinValueValidator(limit_value=1)])
    GENDER_CHOICES = (
        ('female', 'женский'),
        ('male', 'мужской'),
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True)
    REQUIRED_FIELDS = ['first_name', ]
                      #['gender', 'age']

    def __str__(self):
        return self.username


class Music(models.Model):
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    album = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    genre = models.CharField(max_length=50)
    audio = models.FileField(upload_to='audios/%Y/%m/%d/')
    year_published = models.IntegerField()
    popularity = models.IntegerField(default=0)
    new = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Favorites(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    song = models.ForeignKey(Music, on_delete=models.PROTECT)
