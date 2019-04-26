from funding.models import OpportunitySubject

from pyforms_web.widgets.django import ModelAdminWidget

from django.conf import settings
from confapp import conf

class SubjectAdminApp(ModelAdminWidget):
	
	UID 			= 'funding-opportunitiessubject-app'
		
	TITLE 			= 'Subjects'
	MODEL 			= OpportunitySubject
	LIST_DISPLAY 	= ['opportunitysubject_name','opportunitysubject_order']
	SEARCH_FIELDS 	= ['opportunitysubject_name__icontains']

	ORQUESTRA_MENU  	 = 'left>FundingOpportunitiesApp'
	ORQUESTRA_MENU_ORDER = 0
	ORQUESTRA_MENU_ICON  = 'asterisk'
	LAYOUT_POSITION   	 = conf.ORQUESTRA_HOME
	AUTHORIZED_GROUPS 	 = [settings.PERMISSION_EDIT_FUNDING, 'superuser']


	FIELDSETS = ['opportunitysubject_name', 'opportunitysubject_order']