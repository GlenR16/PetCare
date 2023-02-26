from django.db import models
import uuid
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .managers import UserManager
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="home")



STATUS = {
    "PENDING":"Pending",
    "ALLOTTED":"Allotted",
    "RESCUED":"Rescued"
    }

PAY_STATUS = {
    "PENDING":"Pending",
    "SUCCESS":"Success",
    "FAILURE":"Failure"
}

def upload_v(instance,filename):
    return "verification/"+str(uuid.uuid4())+"."+filename.split(".")[-1]

def upload_i(instance,filename):
    return "image/"+str(Animal.objects.all().count()+1)+"."+filename.split(".")[-1]

class Animal(models.Model):
    image = models.ImageField(upload_to=upload_i)
    latitude = models.FloatField()
    longitude = models.FloatField()
    is_valid = models.BooleanField(default=True)
    status = models.CharField(max_length=63,default=STATUS["PENDING"])
    def __str__(self):
        location = geolocator.reverse(str(self.latitude)+","+str(self.longitude))
        return str(location)

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

class Donation(models.Model):
    user = models.CharField(max_length=127)
    message = models.CharField(max_length=511,blank=True,null=True)
    status = models.CharField(max_length=31,default=PAY_STATUS["PENDING"])
    payment_id = models.CharField(max_length=255)
    amount = models.FloatField()
    signature = models.CharField(max_length=255)

    def __str__(self):
        return str(self.user)+" ("+str(self.amount)+")"

class Message(models.Model):
    name = models.CharField(max_length=127)
    email = models.EmailField(max_length=254)
    message = models.TextField()

    def __str__(self):
        return self.name
