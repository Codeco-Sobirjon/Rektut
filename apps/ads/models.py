from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from apps.auth_app.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    subcategory = models.ForeignKey("self", on_delete=models.PROTECT, null=True, blank=True)
    icon = models.ImageField(upload_to="path/", null=True, blank=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    short_name = models.CharField(max_length=4, unique=True, null=True, blank=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    short_name = models.CharField(max_length=30, null=True, blank=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class FieldTypes(models.TextChoices):
    string = ("string", "string")
    integer = ("integer", "integer")
    boolean = ("boolean", "boolean")
    date = ("date", "date")
    time = ("time", "time")
    datetime = ("datetime", "datetime")
    float = ("float", "float")
    image = ("image", "image")
    file = ("file", "file")


class OptionalField(models.Model):
    FieldTypes = FieldTypes
    name = models.CharField(max_length=30, null=True, blank=True)
    key = models.CharField(max_length=12, null=True, blank=True)
    type = models.CharField(max_length=30, choices=FieldTypes.choices, default=FieldTypes.string, null=True, blank=True)
    is_required = models.BooleanField(default=False)
    default = models.TextField(null=True, blank=True)
    max_length = models.IntegerField(null=True, blank=True)
    min_length = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class OptionalFieldThrough(models.Model):
    job = models.ForeignKey('Job', on_delete=models.CASCADE, null=True, blank=True)
    optional_field = models.ForeignKey(OptionalField, on_delete=models.CASCADE, null=True, blank=True)
    value = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to="path/")
    file = models.FileField(null=True, blank=True, upload_to="path/")

    def __str__(self):
        return self.value


class JobStatusChoices(models.TextChoices):
    published = "published", "Published"
    under_review = "under_review", "Under Review"
    approved = "approved", "Approved"
    draft = "draft", "Draft"
    rejected = "rejected", "Rejected"
    archived = "archived", "Archived"
    blocked = "blocked", "Blocked"


class Job(models.Model):
    JobStatusChoices = JobStatusChoices
    title = models.CharField(max_length=200, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.PROTECT, null=True, blank=True)
    description = models.TextField(default="", null=True, blank=True)
    contact_number = models.CharField(max_length=18, null=True, blank=True)
    email = models.EmailField( null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, null=True, blank=True)
    status = models.CharField(max_length=30, default=JobStatusChoices.published, null=True, blank=True)
    photo = models.ImageField(upload_to="path/", null=True, blank=True)
    date_create = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    date_update = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_vip = models.BooleanField(default=False)
    is_top = models.BooleanField(default=False)
    # rate future

    optional_field = models.ManyToManyField(
        OptionalField,
        through=OptionalFieldThrough,
        through_fields=('job', 'optional_field'), null=True, blank=True
    )


