from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Dashboards(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dashboards')
    name = models.CharField(max_length=64)
    extra1_label = models.CharField(max_length=32)
    extra1_state = models.BooleanField(default=False)
    extra2_label = models.CharField(max_length=32)
    extra2_state = models.BooleanField(default=False)
    extra3_label = models.CharField(max_length=32)
    extra3_state = models.BooleanField(default=False)

    def __str__(self):
        return self.name