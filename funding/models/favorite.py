from django.db import models
from django.contrib.auth.models import User

class Favorite(models.Model):

    favorite_id = models.AutoField(primary_key=True)
    
    created     = models.DateTimeField('Created', auto_now_add=True)
    updated     = models.DateTimeField('Updated', auto_now=True)
    active      = models.BooleanField('Active', default=True)

    

    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    funding     = models.ForeignKey('FundingOpportunity', on_delete=models.CASCADE)

    def __unicode__(self):  return self.funding.fundingopportunity_name
    def __str__(self):      return self.funding.fundingopportunity_name

    class Meta:
        ordering = ['funding__fundingopportunity_name']
        db_table = "fund_favorite"

    