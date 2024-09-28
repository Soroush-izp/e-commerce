from django.db import models
from iranian_cities.models import Ostan, Shahrestan
from accounts.models import User

class Address(models.Model):
   user = models.ForeignKey(User, on_delete=models.CASCADE)
   title = models.CharField(max_length=35, null=True, blank=True)
   province = models.ForeignKey(Ostan, on_delete=models.CASCADE)
   city = models.ForeignKey(Shahrestan, on_delete=models.CASCADE)
   postal_code = models.CharField(max_length=20, null=False, blank=False, default='000000')
   phone_number = models.CharField(max_length=15, null=True, blank=True)
   street = models.TextField(max_length=30, null=False, blank=False, default='UNKNOWN')
   address = models.TextField(null=False, blank=False, default='UNKNOWN')
   
   def __str__(self):
      return f"{self.street}, {self.city.name}, {self.province.name}"
