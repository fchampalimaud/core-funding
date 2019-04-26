from django.db import models

class FundingType(models.Model):

    fundingtype_id    = models.AutoField(primary_key=True)
    fundingtype_name  = models.CharField('Funding type', max_length=255)

    class Meta:
        ordering = ['fundingtype_name']
        db_table = "fund_type"

    def __unicode__(self): return self.fundingtype_name
    def __str__(self): return self.fundingtype_name

    @staticmethod
    def autocomplete_search_fields():
        return ("fundingtype_name__icontains",)
