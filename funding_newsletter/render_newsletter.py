import sys,os
from django.utils.dateparse import parse_datetime
from funding_opportunities_models.models  import FundingOpportunity
from django.conf            import settings
from django.utils           import timezone
from django.contrib.auth    import models
from django.core.mail       import EmailMessage
from django.template.loader import render_to_string
from django.utils.timezone import is_aware, make_aware
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


NEW_FUNDS_N_DAYS	 = 5*30 # show new funding opportunities with 
NEW_FUNDS_N_MAX 	 = 8 # Maximum of funds to send
CLOSING_FUNDS_N_DAYS = 30 # number of days required for a fund to be considered a closing fund.
ROLLING_FUNDS_MONTHS = [1,5,9]

def get_aware_datetime(date_str):
	ret = parse_datetime(date_str)
	if not is_aware(ret):
		ret = make_aware(ret)
	return ret


def find_first_monday(year, month):
	d = date(year, 1, 4)  # The Jan 4th must be in week 1  according to ISO
	d = d + relativedelta(months=+month-1)
	d = d + timedelta( days=-d.weekday() )
	if (d.month<month): d = d + timedelta(days=7)
	return d

def render_newsletter(save_flag=True):
	try:
		flagfile = os.path.join(settings.BASE_DIR,'last-run.txt')
		with open(flagfile, 'r') as infile: last_run = get_aware_datetime(infile.readline())
	except:
		last_run = None

	newfunds = FundingOpportunity.objects.all()
	limit_date = timezone.now() + timedelta(days=NEW_FUNDS_N_DAYS)
	newfunds = newfunds.exclude(fundingopportunity_end__gt=limit_date)
	newfunds = newfunds.exclude(fundingopportunity_end__lt=timezone.now())
	newfunds = newfunds.exclude(fundingopportunity_published=True)
	newfunds = newfunds.exclude(fundingopportunity_end=None)
	# Do not include the funds sent in the last email
	if last_run is not None:
		newfunds = newfunds.exclude(fundingopportunity_end__lte=last_run) if last_run is not None else newfunds
	newfunds = newfunds.order_by('fundingopportunity_end', 'fundingopportunity_name' )[:NEW_FUNDS_N_MAX]

	### CLOSING IN 30 DAYS ########################################################################
	closingfunds = FundingOpportunity.objects.all()
	closingfunds = closingfunds.exclude(fundingopportunity_end=None)
	limit_date = timezone.now() + timedelta(days=CLOSING_FUNDS_N_DAYS)
	closingfunds = closingfunds.exclude(fundingopportunity_end__lt=timezone.now())
	closingfunds = closingfunds.exclude(fundingopportunity_end__gt=limit_date)
	closingfunds = closingfunds.order_by('subject','fundingopportunity_end', 'fundingopportunity_name' )
	###############################################################################################

	### ROLLING OPPORTUNITIES #####################################################################
	# They should be generated only on the first monday of May, September and January #############
	###############################################################################################
	month = timezone.now().month

	if month in ROLLING_FUNDS_MONTHS:
		first_monday 	 = find_first_monday(timezone.now().year, month)
		previous_tuesday = first_monday + timedelta(days=-6)

		if previous_tuesday<=timezone.now().date()<=first_monday:	
			rollingfunds = FundingOpportunity.objects.all()
			rollingfunds = rollingfunds.filter(fundingopportunity_end=None)
			rollingfunds = rollingfunds.order_by('subject','fundingopportunity_end', 'fundingopportunity_name' )
		else:
			rollingfunds = []
	else:
		rollingfunds = []
	###############################################################################################

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