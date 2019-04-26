from django.db import models
from django.utils import timezone
from .funding_opportunity import FundingOpportunity
from django.db.models import Q

class OpportunitySubject(models.Model):

    opportunitysubject_id    = models.AutoField(primary_key=True)
    opportunitysubject_name  = models.CharField('Type', max_length=80)
    opportunitysubject_order = models.CharField('Order', max_length=2, null=True, blank=True)

    class Meta:
        ordering = ['opportunitysubject_name']
        db_table = "fund_subject"

    def __unicode__(self): return self.opportunitysubject_name
    def __str__(self): return self.opportunitysubject_name


    def count_funds(self):
        today = timezone.now()
        funds = FundingOpportunity.objects.filter( 
            Q(fundingopportunity_end__gte=today) | Q(fundingopportunity_loideadline__gte=today) 
        ).filter(subject=self)
        return funds.count()

    @staticmethod
    def autocomplete_search_fields():
        return ("opportunitysubject_name__icontains",)
