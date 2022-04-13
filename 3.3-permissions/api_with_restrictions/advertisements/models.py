from django.conf import settings
from django.db import models


class AdvertisementStatusChoices(models.TextChoices):
    """Статусы объявления."""

    OPEN = "OPEN", "Открыто"
    CLOSED = "CLOSED", "Закрыто"
    DRAFT = "DRAFT", "Черновик"


class Advertisement(models.Model):
    """Объявление."""

    title = models.TextField()
    description = models.TextField(default='')
    status = models.TextField(
        choices=AdvertisementStatusChoices.choices,
        default=AdvertisementStatusChoices.OPEN
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='UsersFavorite',
        related_name='favorite',
        null=True,
        blank=True
    )


class UsersFavorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='favorites', on_delete=models.CASCADE)
    advertisement = models.ForeignKey(Advertisement, related_name='favorites', on_delete=models.CASCADE)

    # def __str__(self):
    #     return f'{self.user.id} - {self.advertisement.id}. {self.advertisement.title}'
