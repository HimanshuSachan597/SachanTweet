from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Tweet (models.Model):
     user = models.ForeignKey(User,on_delete=models.CASCADE)
     text = models.TextField(max_length=250)
     photo = models.ImageField(upload_to='Tphotos/',blank=True,null=True)
     create_at = models.DateTimeField(auto_now_add=True)  # ye es vjh se likh rhe hai ki jo bhi kuch create kiya ja uki thime date bhi Aa jaye
     Updated_at = models.DateTimeField(auto_now=True) # aur jb kuchh update ho .....
     
     
     def __str__(self):
        return f'{self.user.username} - {self.text[:10]}'
     
     