from django.db import models


class TeamRole(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default="")
    photo = models.ImageField(upload_to="path/")
    role = models.ForeignKey(TeamRole, on_delete=models.PROTECT)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
