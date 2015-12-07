from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

GENDER_CHOICES = (
                    ('M','Male'),
                    ('F','Female'),
                    ('NS','--')
)      #FIELD CHOICES
class CustomUser(AbstractUser):
    gender = models.CharField(max_length = 2, choices = GENDER_CHOICES , default = GENDER_CHOICES[2][0])
    dob = models.DateField(null = True, blank = True)
    phone_number = models.CharField(max_length = 12 , unique = True , default = '')
    class Meta:
        unique_together = ('email')
        verbose_name = 'User'
