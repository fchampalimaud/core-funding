from django.db import models

class Grantor(models.Model):

    grantor_id    = models.AutoField(primary_key=True)
    grantor_name  = models.CharField('Funding agency', max_length=255)

    class Meta:
        ordering = ['grantor_name']
        db_table = "fund_grantor"

    def __unicode__(self): return self.grantor_name
    def __str__(self): return self.grantor_name

    @staticmethod
    def autocomplete_search_fields():
        return ("grantor_name__icontains",)
