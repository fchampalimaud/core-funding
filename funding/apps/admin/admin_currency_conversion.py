from funding.models import CurrencyConversion

from pyforms_web.widgets.django import ModelAdminWidget

from django.conf import settings
from confapp import conf

class CurrencyConversionAdminApp(ModelAdminWidget):
	

	UID 			= 'currency-conversion-app'
	
	TITLE 			  = 'Currencies conversion'
	MODEL 			  = CurrencyConversion
	LIST_DISPLAY 	  = ['from_currency__currency_name','to_currency__currency_name', 'rate', 'date']
	LIST_FILTER 	  = ['to_currency__currency_name', 'from_currency__currency_name']
	
	ORQUESTRA_MENU  	 = 'left>FundingOpportunitiesApp'
	ORQUESTRA_MENU_ORDER = 0
	ORQUESTRA_MENU_ICON  = 'dollar'
	LAYOUT_POSITION   	 = conf.ORQUESTRA_HOME
	AUTHORIZED_GROUPS 	 = [settings.PERMISSION_EDIT_FUNDING, 'superuser']


