from funding.models import OpportunityTopic

from pyforms_web.widgets.django import ModelAdminWidget

from django.conf import settings
from confapp import conf

class TopicAdminApp(ModelAdminWidget):
	
	UID 			= 'funding-opportunitytopic-app'
	
	TITLE 			= 'Topics'
	MODEL 			= OpportunityTopic
	LIST_DISPLAY 	= ['opportunitytopic_name']
	SEARCH_FIELDS 	= ['opportunitytopic_name__icontains']

	ORQUESTRA_MENU  	 = 'left>FundingOpportunitiesApp'
	ORQUESTRA_MENU_ORDER = 0
	ORQUESTRA_MENU_ICON  = 'certificate'
	LAYOUT_POSITION   	 = conf.ORQUESTRA_HOME
	AUTHORIZED_GROUPS 	 = [settings.PERMISSION_EDIT_FUNDING, 'superuser']

	FIELDSETS = ['opportunitytopic_name']