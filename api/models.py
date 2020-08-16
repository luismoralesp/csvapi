from django.db import models
from .services import Service
from django.core import validators

class CsvDocument(models.Model):
  name = models.CharField(
    max_length=120, 
    unique=True, 
    validators=[validators.validate_slug]
  )
  file = models.FileField(upload_to='uploads')

  def get_model(self):
    return Service.get_model(self.name)
    
    
