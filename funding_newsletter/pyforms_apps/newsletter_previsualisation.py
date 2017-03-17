from funding_opportunities_models.models import FundingOpportunity
from pyforms_web.web.BaseWidget import BaseWidget
from pyforms_web.web.Controls.ControlHtml import ControlHtml
from pyforms_web.web.Controls.ControlButton import ControlButton
from orquestra.plugins import LayoutPositions
from django.utils import timezone
from datetime import timedelta

from funding_newsletter.render_newsletter import render_newsletter

class NewsletterPrevisualisation(BaseWidget):
	

	_uid 			= 'newsletter-previsualisation'
	#groups	 		= ['superuser']
	icon			= 'desktop'
	label 			= 'Newsletter pre-visualisation'
	menu 			= 'top'
	menu_order 		= 10
	layout_position = LayoutPositions.NEW_TAB
	
	def __init__(self):
		super(NewsletterPrevisualisation, self).__init__('Newsletter pre-visualisation')

		self._htmlcontrol = ControlHtml('Pre-visualisation')
		self._refresh_btn = ControlButton('Refresh')
		self.formset 	  = ['_refresh_btn', '_htmlcontrol']

		self._refresh_btn.value = self.__refresh_event

		self._htmlcontrol.value = render_newsletter(False)

	def __refresh_event(self):
		body = render_newsletter(False)
		self._htmlcontrol.value = body
