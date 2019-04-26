from django.db import models

class PaymentFrequency(models.Model):

    paymentfrequency_id    = models.AutoField(primary_key=True)
    paymentfrequency_name  = models.CharField('Payment per', max_length=80)

    class Meta:
        ordering = ['paymentfrequency_name']
        db_table = "fund_paymentfrequency"

    def __unicode__(self): return self.paymentfrequency_name
    def __str__(self): return self.paymentfrequency_name

    @staticmethod
    def autocomplete_search_fields():
        return ("paymentfrequency_name__icontains",)
