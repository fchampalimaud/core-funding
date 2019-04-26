from funding.models import FundingType

from pyforms_web.widgets.django import ModelAdminWidget

from django.conf import settings
from confapp import conf

class FundingTypeAdminApp(ModelAdminWidget):
	
	UID 			= 'funding-type-app'
	
	TITLE 			= 'Funding type'
	MODEL 			= FundingType
	LIST_DISPLAY 	= ['fundingtype_name']
	SEARCH_FIELDS 	= ['fundingtype_name__icontains']

	ORQUESTRA_MENU  	 = 'left>FundingOpportunitiesApp'
	ORQUESTRA_MENU_ORDER = 0
	ORQUESTRA_MENU_ICON  = 'tags'
	LAYOUT_POSITION   	 = conf.ORQUESTRA_HOME
	AUTHORIZED_GROUPS 	 = [settings.PERMISSION_EDIT_FUNDING, 'superuser']

	FIELDSETS = ['fundingtype_name',]