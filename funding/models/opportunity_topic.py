from django.db    import models
from django.utils import timezone
from .funding_opportunity import FundingOpportunity
from django.db.models import Q

class OpportunityTopic(models.Model):

    opportunitytopic_id   = models.AutoField(primary_key=True)
    opportunitytopic_name = models.CharField('Topic', max_length=80)

    class Meta:
        ordering = ['opportunitytopic_name']
        db_table = "fund_topic"

    @staticmethod
    def autocomplete_search_fields():
        return ("opportunitytopic_name__icontains",)


    def __unicode__(self): return self.opportunitytopic_name
    def __str__(self):     return self.opportunitytopic_name

    def count_users(self):
        return self.profile_set.count()

    def count_funds(self):
        today = timezone.now()
        funds = FundingOpportunity.objects.filter( 
            Q(fundingopportunity_end__gte=today) | Q(fundingopportunity_loideadline__gte=today) 
        ).filter(topics=self)
        return funds.count()

    def total_funds(self):
        today = timezone.now()
        funds = FundingOpportunity.objects.filter( 
            Q(fundingopportunity_end__gte=today) | Q(fundingopportunity_loideadline__gte=today) 
        ).filter(topics=self)

        total = 0
        for fund in funds:
            total += fund.total()

        return total