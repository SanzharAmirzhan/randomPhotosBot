from django.db import models

class Photo(models.Model):
    file_id = models.CharField(max_length=250)