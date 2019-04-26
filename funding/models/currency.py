from django.db import models

class CurrencyConversion(models.Model):

    id   = models.AutoField(primary_key=True)
    rate = models.FloatField('Conversion rate')
    date = models.DateTimeField('Date', auto_now_add=True)
    
    from_currency = models.ForeignKey('Currency', on_delete=models.CASCADE, related_name='from_currency', verbose_name='From')
    to_currency   = models.ForeignKey('Currency', on_delete=models.CASCADE, related_name='to_currency', verbose_name='To')

class Currency(models.Model):

    currency_id    = models.AutoField(primary_key=True)
    currency_name  = models.CharField('Currency', max_length=4)

    def __unicode__(self): return self.currency_name
    def __str__(self): return self.currency_name


    @staticmethod
    def autocomplete_search_fields():
        return ("currency_name__icontains",)


    class Meta:
        ordering = ['currency_name']
        db_table = "fund_currency"


    def convert(self, value, to_currency, when):
        try:
            conversion = CurrencyConversion.objects.filter(
                from_currency=self, 
                to_currency=to_currency,
                date__lte=when
            ).order_by('date')[0]
            rate = conversion.rate
        except:
            rate = 0.0
        try:
            return value*rate
        except:
            return 0