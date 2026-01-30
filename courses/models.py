from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class StudentProfile(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    age = models.IntegerField()
    phone = models.IntegerField()
    parent_phone = models.IntegerField()
    def __str__(self):
        return self.user.username

class Course(models.Model):
    teacher = models.ForeignKey(User,on_delete = models.CASCADE)
    title = models.CharField(max_length = 100)
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to = 'images')
    grade = models.CharField(max_length = 100)
    tag = models.CharField(max_length = 100)
    def __str__(self):
        return self.title