import sys,os
sys.path.append("/home/ricardo/bitbucket/core-project/research-core");
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cnp_core_conf.settings")
#import django; django.setup()
from django.core.management import execute_from_command_line

from django.utils.dateparse import parse_datetime
from osp.models             import FundingOpportunity
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

FROM = 'ricardo.ribeiro@neuro.fchampalimaud.org'
TO = (
	'ricardo.ribeiro@neuro.fchampalimaud.org',
	#'preaward.osp@research.fchampalimaud.org', 
	#'joana.lamego@research.fchampalimaud.org',
	#'mariana.santamarta@research.fchampalimaud.org'
)

try:
	with open('last-run.txt', 'r') as infile: last_run = get_aware_datetime(infile.readline())
except:
	last_run = None
	print 'first-run'

if last_run is not None:
	newfunds = FundingOpportunity.objects.all()
	limit_date = timezone.now() + timedelta(days=4*30)
	newfunds = newfunds.exclude(fundingopportunity_end__gt=limit_date)
	newfunds = newfunds.exclude(fundingopportunity_published=True)
	newfunds = newfunds.exclude(fundingopportunity_end=None)
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

	if newfunds.count()>0 or rollingfunds.count()>0 or closingfunds.count()>0:
		body = render_to_string('funding_newsletter/funding-opportunities-newsletter.html', 
			{'newfunds':newfunds, 'rollingfunds':rollingfunds, 'closingfunds':closingfunds })

		msg = EmailMessage('FUNDING OPPORTUNITIES', body, settings.ENDING_CONTRACT_FROM, TO )
		msg.content_subtype = "html"
		msg.send()

		for fund in newfunds: fund.fundingopportunity_published=True; fund.save()

with open('last-run.txt', 'w') as out: out.write(str(timezone.now()))