from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from apps.ads.models import Job
from apps.auth_app.models import CustomUser


class Review(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.TextField(default="")
    first_name = models.CharField(max_length=200)
    email = models.EmailField()
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name
