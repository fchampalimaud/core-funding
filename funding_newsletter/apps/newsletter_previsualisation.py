from pyforms.basewidget import BaseWidget, no_columns
from pyforms.controls   import ControlHtml
from pyforms.controls   import ControlEmail
from pyforms.controls   import ControlButton

from django.core.mail   import EmailMessage
from django.utils import timezone

from django.conf import settings
from confapp import conf

from funding_newsletter.render_newsletter import query_new
from funding_newsletter.render_newsletter import next_monday
from funding_newsletter.render_newsletter import render_newsletter


class AskConfirmationPopup(BaseWidget):
    AUTHORIZED_GROUPS = ['PROFILE: Can edit the funding opportunities', 'superuser']
    LAYOUT_POSITION   = conf.ORQUESTRA_NEW_WINDOW

    def __init__(self, title, message, action):
        super().__init__(title=title)

        self._y_btn = ControlButton('Yes', css='positive', default=action)
        self._n_btn = ControlButton('No', css='negative', default=self.close)

        self.formset = [
            message,
            no_columns('_y_btn', '_n_btn')
        ]


class NewsletterPrevisualisation(BaseWidget):

    UID = 'newsletter-previsualisation'
    TITLE = 'Newsletter'

    AUTHORIZED_GROUPS = ['PROFILE: Can edit the funding opportunities', 'superuser']
    LAYOUT_POSITION = conf.ORQUESTRA_HOME

    ORQUESTRA_MENU = 'left'
    ORQUESTRA_MENU_ORDER = 0
    ORQUESTRA_MENU_ICON = 'desktop'
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._htmlcontrol = ControlHtml('Pre-visualisation')
        self._email = ControlEmail('Email')
        self._send_btn = ControlButton(
            '<i class="mail outline icon"></i>Send Newsletter',
            label_visible=False,
            css='fluid primary',
        )
        self._preview_btn = ControlButton(
            '<i class="refresh icon"></i>Load Current',
            label_visible=False,
            css='fluid',
        )
        self._previewnext_btn = ControlButton(
            '<i class="eye icon"></i>Preview Next',
            label_visible=False,
            css='fluid',
        )
        self._publishlisted_btn = ControlButton(
            '<i class="flag checkered icon"></i>Publish',
            label_visible=False,
            css='fluid red',
            helptext='Press the publish button if you want to mark these fundings opportunities as published, so they do not appear in the next newsletter.'
        )

        self.formset = [
            '_email',
            no_columns('_send_btn', '_preview_btn', '_previewnext_btn', '_publishlisted_btn'),
            '_htmlcontrol'
        ]

        self._send_btn.value = self.__sendto_event
        self._preview_btn.value         = self.__preview_event
        self._previewnext_btn.value     = self.__previewnext_event
        self._publishlisted_btn.value   = self.__publish_event

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
        skip = 0
        date = next_monday(skip).strftime('%A, %B %d')
        self._htmlcontrol.label = "<h3>To be disseminated %s</h3>" % date
        self._htmlcontrol.value = render_newsletter(skip)

        self._send_btn.enabled = True
        self._publishlisted_btn.enabled = True

    def __previewnext_event(self):
        skip = 1
        date = next_monday(skip).strftime('%A, %B %d')
        self._htmlcontrol.label = "<h3>To be disseminated %s</h3>" % date
        self._htmlcontrol.value = render_newsletter(skip)

        self._send_btn.enabled = False
        self._publishlisted_btn.enabled = False

    def __publish_event(self):

        def publish():
            for o in newfunds:
                o.fundingopportunity_published = True
                o.save()
            popup.close()
            self.__preview_event()

        newfunds = query_new()

        popup = AskConfirmationPopup(
            title=("Are you sure you want to mark the following"
                   " Opportunities as published?"),
            message="".join(
                map(lambda s: "<li>%s</li>" % s, map(str, newfunds))
            ),
            action=publish,
        )