from funding_opportunities_models.models import FundingOpportunity
from pyforms_web.web.basewidget import BaseWidget, no_columns
from pyforms_web.web.controls.ControlHtml import ControlHtml
from pyforms_web.web.controls.ControlEmail import ControlEmail
from pyforms_web.web.controls.ControlButton import ControlButton
from orquestra.plugins import LayoutPositions
from django.core.mail import EmailMessage
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

from funding_newsletter.render_newsletter import next_monday
from funding_newsletter.render_newsletter import render_newsletter


class NewsletterPrevisualisation(BaseWidget):

    UID = 'newsletter-previsualisation'

    AUTHORIZED_GROUPS = ['PROFILE: Can edit the funding opportunities']

    TITLE = 'Newsletter pre-visualisation'
    ORQUESTRA_MENU = 'left'
    ORQUESTRA_MENU_ORDER = 0
    ORQUESTRA_MENU_ICON = 'desktop'
    LAYOUT_POSITION = LayoutPositions.HOME

    def __init__(self):
        super(NewsletterPrevisualisation, self).__init__(self.TITLE)

        self._htmlcontrol = ControlHtml('Pre-visualisation')
        self._email = ControlEmail('Email')
        self._send_btn = ControlButton(
            '<i class="mail outline icon"></i>Send Newsletter',
            label_visible=False,
            css='primary',
        )
        self._preview_btn = ControlButton(
            '<i class="refresh icon"></i>Refresh',
            label_visible=False,
            css='',
        )
        self._previewnext_btn = ControlButton(
            '<i class="eye icon"></i>Preview Next',
            label_visible=False,
            css='',
        )

        self.formset = [
            '_email',
            no_columns('_send_btn', '_preview_btn', '_previewnext_btn'),
            '_htmlcontrol'
        ]

        self._send_btn.value = self.__sendto_event
        self._preview_btn.value = self.__preview_event
        self._previewnext_btn.value = self.__previewnext_event

        self.__preview_event()
        self._email.hide()

    def __sendto_event(self):

        if self._email.visible is False:
            self._email.show()
        elif not self._email.value:
            self.alert('Please specify an email address', 'Error')
        else:
            body = render_newsletter()
            try:
                msg = EmailMessage(
                    settings.FUNDING_OPPORTUNITIES_EMAIL_SUBJECT.format(
                        datetime=timezone.now().strftime('%Y.%m.%d')),
                    body,
                    settings.EMAIL_FROM,
                    (self._email.value,)
                )
                msg.content_subtype = "html"
                msg.send()
                self.success('Email sent with success', 'Success')
                self._email.hide()
            except Exception as e:
                self.alert(str(e), 'Error')

    def __preview_event(self):
        step = 1
        date = next_monday(step).strftime('%A, %B %d')
        self._htmlcontrol.label = "To be disseminated %s" % date
        self._htmlcontrol.value = render_newsletter(step)
        self._send_btn.enabled = True

    def __previewnext_event(self):
        step = 2
        date = next_monday(step).strftime('%A, %B %d')
        self._htmlcontrol.label = "To be disseminated %s" % date
        self._htmlcontrol.value = render_newsletter(step)
        self._send_btn.enabled = False
