from funding.models import FundingOpportunity, OpportunitySubject
from django.shortcuts 	import render_to_response
from django.http 		import HttpResponse
from django.utils	 	import timezone
from datetime 			import timedelta
from django.shortcuts 	import redirect
from django.conf 		import settings

try:
	from django.utils import simplejson
except:
	import json as simplejson


def funding_opportunities_timeline(request):
	template = 'timeline/funding-opportunities.html'
	subjects = OpportunitySubject.objects.all().order_by('opportunitysubject_name')
	response = render_to_response( template, {'subjects': subjects} )
	return response

def funding_opportunities_json(request):
	template = 'timeline/funding-opportunities.html'

	today = timezone.now()
	funds = FundingOpportunity.objects.filter(fundingopportunity_end__gte=today).order_by('fundingopportunity_end')
	user = request.user
	#groups = user.groups.all()

	res = []
	for fund in funds:
		classes = []
		#if fund.groups.filter(group=groups).exists(): classes.append('mine')
		classes.append( 'subject'+str(fund.subject.pk) )
		
		two_weeks_ago = timezone.now() + timedelta(days=-14) 
		if fund.fundingopportunity_createdon>=two_weeks_ago: classes.append('new')

		obj = { 
			'classes':		' '.join(classes),
			"pk": 			fund.pk,
			"title": 		fund.fundingopportunity_name,
			"date":  		fund.fundingopportunity_end.isoformat(),
			"display_date":	fund.fundingopportunity_end.strftime("%d. %B"),
			"enddate":  	fund.fundingopportunity_end.strftime("%d. %B %Y"),
    		"grantor":		fund.financingAgency.grantor_name,
    		"subject":		fund.subject.opportunitysubject_name,
			"body":			fund.fundingopportunity_brifdesc,
			"read_more":	fund.fundingopportunity_link,
			"topics":		', '.join([str(x) for x in fund.topics.all()]),
		}
		#if fund.financingAgency.grantor_icon: obj['photo_url'] = "/media/{0}".format( fund.financingAgency.grantor_icon )
		 
		res.append(obj)

	return HttpResponse(simplejson.dumps(res), content_type='application/json')

