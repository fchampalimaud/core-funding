from funding_opportunities_models.models import FundingOpportunity
from pyforms_web.web.BaseWidget import BaseWidget
from pyforms_web.web.Controls.ControlHtml import ControlHtml
from pyforms_web.web.Controls.ControlEmail import ControlEmail
from pyforms_web.web.Controls.ControlButton import ControlButton
from orquestra.plugins import LayoutPositions
from django.core.mail       import EmailMessage
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

from funding_newsletter.render_newsletter import render_newsletter

class NewsletterPrevisualisation(BaseWidget):
	

	_uid 			= 'newsletter-previsualisation'
	groups	 		= ['PROFILE: Can edit the funding opportunities']
	icon			= 'desktop'
	label 			= 'Newsletter pre-visualisation'
	menu 			= 'top'
	menu_order 		= 10
	layout_position = LayoutPositions.NEW_TAB
	
	def __init__(self):
		super(NewsletterPrevisualisation, self).__init__(self.label)

		self._htmlcontrol = ControlHtml('Pre-visualisation')
		self._email		  = ControlEmail('Email')
		self._refresh_btn = ControlButton('<i class="refresh icon"></i> Reload')
		self._sendto_btn  = ControlButton('<i class="mail outline icon"></i> Sent to')
		self.formset 	  = [
			('_email', '_sendto_btn','_refresh_btn' ),
			'_htmlcontrol'
		]

		self._refresh_btn.value = self.__refresh_event
		self._sendto_btn.value  = self.__sendto_event

		#self._refresh_btn.include_label = False
		#self._refresh_btn.css = 'basic mini primary'
		#self._sendto_btn.include_label = False
		#self._sendto_btn.css = 'basic mini primary'

		self._htmlcontrol.value = render_newsletter(False)
		self._email.hide()

	def __sendto_event(self):
		if self._email.visible==False:
			self._email.show()
		else:
			body = render_newsletter(False)
			try:
				msg = EmailMessage(
					settings.FUNDING_OPPORTUNITIES_EMAIL_SUBJECT, 
					body, 
					settings.EMAIL_FROM, 
					(self._email.value,) )
				msg.content_subtype = "html"
				msg.send()
				self.success('Email sent with success','Success')
				self._email.hide()
			except Exception as e:
				self.alert(str(e),'Error')	
			

	def __refresh_event(self):
		body = render_newsletter(False)
		self._htmlcontrol.value = body
