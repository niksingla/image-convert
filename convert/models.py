from django.db import models

# Create your models here.

class FileUpload(models.Model):
    image_name= models.CharField(max_length=200, default="None")
    file_field = models.FileField(upload_to="uploads/")
    def __str__(self):  
        return self.image_name  
