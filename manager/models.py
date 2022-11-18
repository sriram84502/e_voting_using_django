from distutils.command.upload import upload
from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser,User
import uuid
from django.core.validators import RegexValidator

# Create your models here.
phone_validator = RegexValidator(r"^[0-9]{10}$", "The phone number provided is invalid")
aadhar_validator = RegexValidator(r"^[0-9]{12}$", "The aadhar number provided is invalid")

class CustomUser(AbstractUser):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15,validators=[phone_validator],unique=True)
    is_phone_verified = models.BooleanField(default=False)
    username = models.CharField(max_length=16,validators=[aadhar_validator],unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    district = models.CharField(max_length=50)
    mandal = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    def save(self,*args, **kwargs):
        self.district = str(self.district).lower()
        self.mandal = str(self.mandal).lower()
        super(CustomUser,self).save(*args, **kwargs)


class Profile(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name="profile")
    phone1=models.CharField(max_length=10)
    aadhar1=models.CharField(max_length=12)
    otp=models.CharField(max_length=100,null=True,blank=True)
    uid=models.UUIDField(default=uuid.uuid4)



class participants(models.Model):
    name=models.CharField(max_length=100)
    image=models.ImageField(upload_to='img')
    symbol=models.ImageField(upload_to='img')
    party=models.CharField(max_length=100)
    district=models.CharField(max_length=50)
    mandal=models.CharField(max_length=50)
    father=models.CharField(max_length=100)
    spouse=models.CharField(max_length=100)
    qualification=models.CharField(max_length=100)
    profession=models.CharField(max_length=100)
    positions=models.CharField(max_length=100,default="none")
    intrests=models.CharField(max_length=100,default="none")
    phone=models.CharField(max_length=10)
    address=models.CharField(max_length=100)
    votes=models.IntegerField(default=0)

    class Meta:
        ordering = ('-votes',)

    
class Voters(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    
class Votingrelease(models.Model):
    voting=models.BooleanField(default=False)
    time=models.DateField(auto_now_add=False, blank=True, null=True)

class Resultrelease(models.Model):
    result=models.BooleanField(default=False)
    time=models.DateField(auto_now_add=False, blank=True, null=True)