from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date, time, datetime

class User(AbstractUser):
    is_user = models.BooleanField(default=True)
    
    def __str__(self):
        return self.username

class Audio(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, null=True)
    file_text = models.TextField(null=True, blank=True)
    audio_file = models.FileField(upload_to='audio/')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    date = models.DateTimeField(null=True, blank=True, auto_now_add=True)

    def __str__(self):
        return self.name
    
class Notes(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, null=True)
    note = models.TextField()
    audio = models.ForeignKey(Audio, null=True, blank=True, on_delete=models.CASCADE)
    file_audio = models.TextField(null=True, blank=True,)
    file_text = models.TextField(max_length=45, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(null=True, blank=True, auto_now_add=True)

    def __str__(self):
        return self.name


class Supporting_Doc(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, null=True)
    supporting_doc = models.FileField(null=True, blank=True, upload_to='suporting_files/')
    note = models.ForeignKey(Notes, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Group(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notes = models.ManyToManyField(Notes)
    
    def __str__(self):
        return self.name

