import sys,os
from django.utils.dateparse import parse_datetime
from funding_opportunities_models.models  import FundingOpportunity
from django.conf            import settings
from django.utils           import timezone
from django.contrib.auth    import models
from django.core.mail       import EmailMessage
from django.template.loader import render_to_string
from django.utils.timezone import is_aware, make_aware
from datetime import timedelta

def get_aware_datetime(date_str):
	ret = parse_datetime(date_str)
	if not is_aware(ret):
		ret = make_aware(ret)
	return ret

def render_newsletter(save_flag=True):
	try:
		flagfile = os.path.join(settings.BASE_DIR,'last-run.txt')
		with open(flagfile, 'r') as infile: last_run = get_aware_datetime(infile.readline())
	except:
		last_run = None

	newfunds = FundingOpportunity.objects.all()
	limit_date = timezone.now() + timedelta(days=4*30)
	newfunds = newfunds.exclude(fundingopportunity_end__gt=limit_date)
	newfunds = newfunds.exclude(fundingopportunity_published=True)
	newfunds = newfunds.exclude(fundingopportunity_end=None)
	if last_run is not None:
		newfunds = newfunds.exclude(fundingopportunity_end__lte=last_run) if last_run is not None else newfunds
	newfunds = newfunds.order_by('fundingopportunity_end', 'fundingopportunity_name' )[:10]

	rollingfunds = FundingOpportunity.objects.all()
	rollingfunds = rollingfunds.filter(fundingopportunity_end=None)
	rollingfunds = rollingfunds.order_by('fundingopportunity_end', 'fundingopportunity_name' )

	closingfunds = FundingOpportunity.objects.all()
	closingfunds = closingfunds.exclude(fundingopportunity_end=None)
	limit_date = timezone.now() + timedelta(days=15)
	closingfunds = closingfunds.exclude(fundingopportunity_end__lt=timezone.now())
	closingfunds = closingfunds.exclude(fundingopportunity_end__gt=limit_date)
	closingfunds = closingfunds.order_by('fundingopportunity_end', 'fundingopportunity_name' )

	body = render_to_string(
		'funding_newsletter/funding-opportunities-newsletter.html', 
		{
			'newfunds':		newfunds,
			'rollingfunds':	rollingfunds,
			'closingfunds':	closingfunds
		}
	)

	if save_flag:
		with open('last-run.txt', 'w') as out: out.write(str(timezone.now()))

	return body