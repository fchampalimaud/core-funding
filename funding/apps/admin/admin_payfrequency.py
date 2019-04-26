from funding.models import PaymentFrequency

from pyforms_web.widgets.django import ModelAdminWidget

from django.conf import settings
from confapp import conf

class PayFrequencyAdminApp(ModelAdminWidget):
	
	UID 			= 'funding-paymentfrequency-app'
		
	TITLE 			= 'Payments types'
	MODEL 			= PaymentFrequency
	LIST_DISPLAY 	= ['paymentfrequency_name']
	SEARCH_FIELDS 	= ['paymentfrequency_name__icontains']

	ORQUESTRA_MENU  	 = 'left>FundingOpportunitiesApp'
	ORQUESTRA_MENU_ORDER = 0
	ORQUESTRA_MENU_ICON  = 'hourglass half'
	LAYOUT_POSITION   	 = conf.ORQUESTRA_HOME
	AUTHORIZED_GROUPS 	 = [settings.PERMISSION_EDIT_FUNDING, 'superuser']

	FIELDSETS = ['paymentfrequency_name',]