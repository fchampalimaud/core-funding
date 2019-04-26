from django.conf.urls import url
from .views import funding_opportunities_timeline, funding_opportunities_json

urlpatterns =  [
	url(r'^fundingopportunities-timeline/$', 		funding_opportunities_timeline),
	url(r'^fundingopportunities-timeline/ajax/$', 	funding_opportunities_json),
]