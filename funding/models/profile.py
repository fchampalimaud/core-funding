from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):

    profile_id = models.AutoField(primary_key=True)
    
    topics   = models.ManyToManyField('OpportunityTopic',   verbose_name='Topics', blank=True)
    user     = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['user']
        db_table = "fund_profile"