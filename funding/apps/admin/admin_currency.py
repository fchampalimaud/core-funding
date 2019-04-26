from funding.models import Currency

from pyforms_web.widgets.django import ModelAdminWidget

from django.conf import settings
from confapp import conf

class CurrencyAdminApp(ModelAdminWidget):
	

	UID 			  = 'funding-currency-app'
	
	TITLE 			  = 'Currencies'
	MODEL 			  = Currency
	LIST_DISPLAY 	  = ['currency_name']
	SEARCH_FIELDS 	  = ['currency_name__icontains']
	
	ORQUESTRA_MENU  	 = 'left>FundingOpportunitiesApp'
	ORQUESTRA_MENU_ORDER = 0
	ORQUESTRA_MENU_ICON  = 'dollar'
	LAYOUT_POSITION   	 = conf.ORQUESTRA_HOME
	AUTHORIZED_GROUPS 	 = [settings.PERMISSION_EDIT_FUNDING, 'superuser']

	FIELDSETS = ['currency_name',]