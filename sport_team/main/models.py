from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.db.models import Avg
from django.conf import settings
from django.db import models
from pathlib import Path
from typing import Optional
from PIL import Image, ImageOps


class Game(models.Model):
    starts_at = models.DateTimeField(blank=True, null=True, verbose_name='Початок')
    created_at = models.DateTimeField(auto_now_add=True)
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name='Місто')
    place = models.CharField(max_length=100, blank=True, null=True, verbose_name='Місце')
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    note = models.TextField(blank=True, verbose_name='Додаткова інформація')
    max_players = models.IntegerField(verbose_name='Максимум гравців', validators=[
            MinValueValidator(2),
        ])
    teams_num = models.IntegerField(verbose_name='Кількість команд', validators=[
            MinValueValidator(2),
        ])
    players = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='Гравці', related_name='games')

    def __str__(self):
        dt = self.created_at.strftime('%m-%d-%Y')
        return ' '.join(s for s in (self.city, self.place, dt) if s)


class Team(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    admins = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='admin_teams')
    players = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='teams')


class PlayerRating(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    from_player = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='given_ratings'
    )

    to_player = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_ratings'
    )
    rating = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['from_player', 'to_player'],
                name='unique_player_rating'
            )
        ]


def player_avatar_path(instance: 'Player', filename: str):
    ext = Path(filename).suffix
    return f'avatars/{instance.pk}{ext}'


class Player(AbstractUser):
    avatar = models.ImageField(upload_to=player_avatar_path, blank=True, default='default-avatar.png', verbose_name='Аватар')
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50, verbose_name="Ім'я", blank=True)
    last_name = models.CharField(max_length=50, verbose_name="Прізвище", blank=True)
    username = models.CharField(max_length=150, unique=True, verbose_name="Логін")

    class Meta(AbstractUser.Meta):
        verbose_name = 'Гравець'
    
    @property
    def avg_rating(self) -> Optional[float]:
        result = self.received_ratings.aggregate(
            avg=Avg('rating')
        )

        return result['avg']
    
    def save(self, *args, **kwargs):
        if not self.avatar:
            self.avatar = 'default-avatar.png'

        super().save(*args, **kwargs)

        if self.avatar and self.avatar.name != 'default-avatar.png':
            img = Image.open(self.avatar.path)
            img = img.convert("RGB")

            # обрізає та масштабує до точного розміру
            img = ImageOps.fit(
                img,
                (300, 300),
                method=Image.Resampling.LANCZOS
            )

            img.save(self.avatar.path, quality=90)