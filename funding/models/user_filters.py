from django.db import models
from django.contrib.auth.models import User

class UserFilters(models.Model):

    id       = models.AutoField(primary_key=True)
    created  = models.DateTimeField('Created', auto_now_add=True)
    
    topics   = models.ManyToManyField('OpportunityTopic',   verbose_name='Topics', blank=True)
    subjects = models.ManyToManyField('OpportunitySubject', verbose_name='Subjects', blank=True)
    user     = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']
        db_table = "fund_usersfilters"