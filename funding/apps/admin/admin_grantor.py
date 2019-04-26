from funding.models import Grantor

from pyforms_web.widgets.django import ModelAdminWidget

from django.conf import settings
from confapp import conf

class GrantorAdminApp(ModelAdminWidget):
	
	UID 			= 'funding-grantor-app'
	
	TITLE 			= 'Agencies'
	MODEL 			= Grantor
	LIST_DISPLAY 	= ['grantor_name']
	SEARCH_FIELDS 	= ['grantor_name__icontains']

	ORQUESTRA_MENU  	 = 'left>FundingOpportunitiesApp'
	ORQUESTRA_MENU_ORDER = 0
	ORQUESTRA_MENU_ICON  = 'suitcase'
	LAYOUT_POSITION   	 = conf.ORQUESTRA_HOME
	AUTHORIZED_GROUPS 	 = [settings.PERMISSION_EDIT_FUNDING, 'superuser']

	FIELDSETS = ['grantor_name',]