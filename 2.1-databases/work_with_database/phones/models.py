from django.db import models
from django.utils.text import slugify


class Phone(models.Model):
    name = models.CharField(max_length=255)
    image = models.FileField()
    price = models.IntegerField()
    release_date = models.DateField()
    lte_exists = models.BooleanField()
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
