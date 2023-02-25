from django.db import models
import uuid
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .managers import UserManager

STATUS = {}

def upload_v(instance,filename):
    return "verification/"+str(uuid.uuid4())+"."+filename.split(".")[-1]

def upload_i(instance,filename):
    return "image/"+str(Animal.objects.all().count()+1)+"."+filename.split(".")[-1]

class Animal(models.Model):
    image = models.ImageField(upload_to=upload_i)
    latitude = models.FloatField()
    longitude = models.FloatField()
    status = models.CharField(max_length=63)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("Email Address",unique=True,max_length=127)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    verification_file = models.FileField(upload_to=upload_v)
    about = models.CharField(max_length=1023)
    is_verified = models.BooleanField(default=False)
    latitude = models.FloatField()
    longitude = models.FloatField()
    active_members = models.IntegerField()
    tickets = models.ManyToManyField(Animal,blank=True)
    address = models.CharField(max_length=255)
    website = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["name","phone","latitude","longitude","active_members","address","website"]

    def __str__(self):
        return self.name