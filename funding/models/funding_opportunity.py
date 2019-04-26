from django.db import models
from django.utils import timezone
from datetime import timedelta
from .currency import Currency

from django.db import models
from django.utils import timezone
from django.db.models import Q

class FundingOpportunityQuerySet(models.QuerySet):

    def recently_updated(self):
        """
        Filter only active people
        """
        now = timezone.now() - timedelta(weeks=1)
        return self.filter(updated__gte=now)


class FundingOpportunity(models.Model):

    fundingopportunity_id           = models.AutoField(primary_key=True)
    fundingopportunity_published    = models.BooleanField('Published')   
    fundingopportunity_rolling      = models.BooleanField('Rolling')
    fundingopportunity_name         = models.CharField('Fund. opportunity name', max_length=255)
    fundingopportunity_end          = models.DateTimeField('Deadline (Lisbon time)', blank=True, null=True)
    fundingopportunity_value        = models.IntegerField('Funding value',      blank=True,     null=True)
    fundingopportunity_duration     = models.IntegerField('Duration in months', blank=True,     null=True)
    fundingopportunity_eligibility  = models.TextField('Eligibility',       blank=True,     null=True)
    fundingopportunity_scope        = models.TextField('Scope',             blank=True,     null=True)
    fundingopportunity_brifdesc     = models.TextField('Observations',      blank=True,     null=True)
    fundingopportunity_desc         = models.TextField('Description',       blank=True,     null=True)
    fundingopportunity_createdon    = models.DateTimeField('Created on',    auto_now_add=True)
    fundingopportunity_updatedon    = models.DateTimeField('Created on',    auto_now_add=True)
    fundingopportunity_link         = models.URLField('Link',               max_length=255, blank=True, null=True)
    fundingopportunity_loideadline  = models.DateTimeField('LOI deadline', blank=True, null=True)
    fundingopportunity_fullproposal = models.DateTimeField('Full proposal deadline', blank=True, null=True)

    created     = models.DateTimeField('Created', auto_now_add=True)
    updated     = models.DateTimeField('Updated', auto_now=True)
    
    currency         = models.ForeignKey('Currency',            on_delete=models.CASCADE, verbose_name='Currency')
    paymentfrequency = models.ForeignKey('PaymentFrequency',    on_delete=models.CASCADE, verbose_name='Payment frequency', blank=True, null=True)
    subject          = models.ForeignKey('OpportunitySubject',  on_delete=models.CASCADE, verbose_name='Subject')
    financingAgency  = models.ForeignKey('Grantor',             on_delete=models.CASCADE, verbose_name='Financing agency')
    fundingtype      = models.ForeignKey('FundingType',         on_delete=models.CASCADE, blank=True, null=True, verbose_name='Funding type')
    
    topics = models.ManyToManyField('OpportunityTopic', verbose_name='Topics', blank=True)


    objects = FundingOpportunityQuerySet.as_manager()

    def __str__(self): return self.fundingopportunity_name

    class Meta:
        verbose_name_plural = "Funding opportunities"
        get_latest_by       = "fundingopportunity_end"
        ordering            = ['fundingopportunity_end']
        db_table            = "fund_opportunity"

    def total(self, to_currency=None, when=None):
        to_currency = Currency.objects.get(currency_name='EUR') if to_currency is None else to_currency
            
        value = self.fundingopportunity_value
        when  = timezone.now() if when is None else when
        return self.currency.convert(value, to_currency, when)


    def funding_value(self):
        return '{:20.,2f}'.format(18446744073709551616.0)

    def copy(self):
        try:
            return """<a class="btn btn-success" 
                    href='/osp/fundingopportunity/{0}/copy' >
                    Make a copy
                    </a>""".format(self.pk)
        except ObjectDoesNotExist:
            return "Not created yet"
    copy.short_description = 'Copy'
    copy.allow_tags = True