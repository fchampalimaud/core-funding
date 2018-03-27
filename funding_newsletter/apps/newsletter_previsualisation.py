from funding_opportunities_models.models import FundingOpportunity
from pyforms_web.web.basewidget import BaseWidget, no_columns
from pyforms_web.web.controls.ControlHtml import ControlHtml
from pyforms_web.web.controls.ControlEmail import ControlEmail
from pyforms_web.web.controls.ControlButton import ControlButton
from orquestra.plugins import LayoutPositions
from django.core.mail       import EmailMessage
from django.utils import timezone
from datetime import timedelta
from django.conf import settings


from funding_newsletter.render_newsletter import render_newsletter

class NewsletterPrevisualisation(BaseWidget):


	UID 			= 'newsletter-previsualisation'

	AUTHORIZED_GROUPS = ['PROFILE: Can edit the funding opportunities']

	TITLE 				 = 'Newsletter pre-visualisation'
	ORQUESTRA_MENU 		 = 'left'
	ORQUESTRA_MENU_ORDER = 0
	ORQUESTRA_MENU_ICON	 = 'desktop'
	LAYOUT_POSITION 	 = LayoutPositions.HOME

	def __init__(self):
		super(NewsletterPrevisualisation, self).__init__(self.TITLE)

		self._htmlcontrol = ControlHtml('Pre-visualisation')
		self._email		  = ControlEmail('Email')
		self._refresh_btn = ControlButton('<i class="refresh icon"></i> Reload')
		self._sendto_btn  = ControlButton('<i class="mail outline icon"></i> Send to')
		self._sendtotest_btn  = ControlButton('<i class="mail outline icon"></i> Send Test')
		self._previewnext_btn  = ControlButton('<i class="eye icon"></i> Preview Next')
		self.formset 	  = [
			'_email',
			(
				# BaseWidget.FORM_NO_ROW_ALIGNMENT,
				'_sendto_btn', '_sendtotest_btn',
				'_refresh_btn', '_previewnext_btn',
			),
			'_htmlcontrol'
		]

		self._refresh_btn.value = self.__refresh_event
		self._previewnext_btn.value = self.__previewnext_event
		self._sendto_btn.value  = self.__sendto_event

		self._refresh_btn.include_label = False
		#self._refresh_btn.css = 'basic mini primary'
		self._sendto_btn.include_label = False
		self._sendtotest_btn.css = 'basic secondary'
		self._refresh_btn.css = 'basic secondary'
		self._previewnext_btn.css = 'basic secondary'

		self._htmlcontrol.value = render_newsletter(False)
		self._email.hide()

	def __sendto_event(self):
		if self._email.visible==False:
			self._email.show()
		else:
			body = render_newsletter(False)
			try:
				msg = EmailMessage(
					settings.FUNDING_OPPORTUNITIES_EMAIL_SUBJECT.format(datetime=timezone.now().strftime('%Y.%m.%d')),
					body,
					settings.EMAIL_FROM,
					(self._email.value,)
				)
				msg.content_subtype = "html"
				msg.send()
				self.success('Email sent with success','Success')
				self._email.hide()
			except Exception as e:
				self.alert(str(e),'Error')


	def __refresh_event(self):
		body = render_newsletter(False)
		self._htmlcontrol.value = body

	def __previewnext_event(self):
		body = render_newsletter(True)
		self._htmlcontrol.value = body
