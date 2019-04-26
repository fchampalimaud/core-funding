from funding.models import FundingOpportunity

from django.utils import timezone
from datetime     import timedelta
from calendar     import monthrange

from pyforms_web.web.middleware import PyFormsMiddleware
from pyforms_web.widgets.django import ModelAdminWidget
from pyforms_web.widgets.django import ModelFormWidget

from pyforms.basewidget import BaseWidget, segment, no_columns
from pyforms.controls   import ControlCheckBox
from pyforms.controls   import ControlButton

from django.conf import settings
from confapp     import conf

class EditFundingOpportunitiesApp(ModelFormWidget):

    AUTHORIZED_GROUPS = [settings.PERMISSION_EDIT_FUNDING, 'superuser']

    TITLE = "Edit opportunities"
    MODEL = FundingOpportunity

    FIELDSETS = [
        'h2:Opportunity details',
        segment([
            ('subject','fundingopportunity_published','fundingopportunity_rolling'),
            ('fundingopportunity_name','fundingopportunity_end'),
            ('_loi','fundingopportunity_loideadline', 'fundingopportunity_fullproposal'),
            ('fundingopportunity_link','topics'),
        ]),
        'h2:Financing info',
        segment([
            ('financingAgency','currency','paymentfrequency'),
            ('fundingtype','fundingopportunity_value','fundingopportunity_duration'),
        ]),
        'h2:Description',
        segment([
            'fundingopportunity_eligibility',
            'fundingopportunity_scope',
            'fundingopportunity_brifdesc',
        ])
    ]

    def __init__(self, *args, **kwargs):
        self._loi     = ControlCheckBox('LOI', changed_event=self.__loi_changed_event)
        self._copybtn = ControlButton('Copy',  default=self.__copybtn_event, label_visible=False, css='red')

        super().__init__(*args, **kwargs)

        self.fundingopportunity_loideadline.hide()
        self.fundingopportunity_fullproposal.hide()
        self.__fundingtype_changed_evt()
        self.__loi_changed_event()
        self.fundingtype.changed_event = self.__fundingtype_changed_evt


    def __fundingtype_changed_evt(self):
        if self.fundingtype.value==None:
            self.fundingopportunity_value.show()

        else:
            self.fundingopportunity_value.hide()
            self.fundingopportunity_value.value = None


    def __loi_changed_event(self):
        if self._loi.value:
            self.fundingopportunity_loideadline.show()
            self.fundingopportunity_fullproposal.show()
        else:
            self.fundingopportunity_loideadline.value = None
            self.fundingopportunity_fullproposal.value = None
            self.fundingopportunity_loideadline.hide()
            self.fundingopportunity_fullproposal.hide()

    def delete_event(self):
        res = super(EditFundingOpportunitiesApp, self).delete_event()
        self._copybtn.hide()
        return res

    def save_event(self, obj, new_object):
        res = super(EditFundingOpportunitiesApp, self).save_event(obj, new_object)
        self._copybtn.show()
        return res

    def show_create_form(self):
        super(EditFundingOpportunitiesApp, self).show_create_form()
        self._copybtn.hide()

    def show_edit_form(self, pk=None):
        super(EditFundingOpportunitiesApp, self).show_edit_form(pk)
        self._copybtn.show()

        if self.fundingopportunity_loideadline.value is None and self.fundingopportunity_fullproposal.value is None:
            self.fundingopportunity_loideadline.hide()
            self.fundingopportunity_fullproposal.hide()
            self._loi.value = False
        else:
            self._loi.value = True

    def get_buttons_row(self):
        return [no_columns('_save_btn', '_create_btn', '_cancel_btn', ' ' ,'_copybtn',' ' ,'_remove_btn')]

    def __copybtn_event(self):
        obj     = self.model_object
        obj.pk  = None
        obj.fundingopportunity_name += ' (copy)'
        obj.save()

        for topic in self.model_object.topics.all():
            obj.topics.add(topic)

        app = PyFormsMiddleware.get_instance('opportunities-app')
        app.populate_list()
        app.show_edit_form(obj.pk)
        self.info('Copied')



class EditFundingApp(EditFundingOpportunitiesApp):

    LAYOUT_POSITION = conf.ORQUESTRA_NEW_TAB

    def __init__(self, fund_pk):
        super(EditFundingApp,self).__init__(
            title=str(FundingOpportunity.objects.get(pk=fund_pk)),
            pk=fund_pk
        )

    def get_buttons_row(self):
        return [no_columns('_save_btn',  '_create_btn', ' ' ,'_copybtn',' ' ,'_remove_btn')]


    def delete_event(self):
        res = super(EditFundingApp, self).delete_event()
        if res:
            app = PyFormsMiddleware.get_instance('opportunities-app')
            app.populate_list()
        return res

    def save_event(self, obj, new_object):
        res = super(EditFundingApp, self).save_event(obj, new_object)
        if res:
            app = PyFormsMiddleware.get_instance('opportunities-app')
            app.populate_list()
        return res





class FundingOpportunitiesApp(ModelAdminWidget):

    UID            = 'opportunities-app'

    ORQUESTRA_MENU       = 'left'
    ORQUESTRA_MENU_ORDER = 2
    ORQUESTRA_MENU_ICON  = 'money'
    AUTHORIZED_GROUPS    = [settings.PERMISSION_EDIT_FUNDING, 'superuser']
    LAYOUT_POSITION      = conf.ORQUESTRA_HOME

    TITLE           = "Edit funds"
    MODEL           = FundingOpportunity
    EDITFORM_CLASS  = EditFundingOpportunitiesApp
    LIST_DISPLAY    = ['fundingopportunity_name', 'subject__opportunitysubject_name','financingAgency__grantor_name', 'fundingopportunity_end',
                       'fundingopportunity_loideadline','fundingopportunity_value',
                       'currency__currency_name','paymentfrequency__paymentfrequency_name','fundingopportunity_published']
    LIST_FILTER     = ['subject__opportunitysubject_name','financingAgency__grantor_name', 'fundingopportunity_end',
                       'fundingopportunity_loideadline','fundingtype__fundingtype_name',
                       'topics__opportunitytopic_name', 'fundingopportunity_published',
                       'fundingopportunity_rolling']
    SEARCH_FIELDS   = ['fundingopportunity_name__icontains', 'fundingopportunity_eligibility__icontains', 'fundingopportunity_scope__icontains']

    def __init__(self, *args, **kwargs):

        self._recently_updated= ControlCheckBox(
            'Updated recently',
            default=False,
            label_visible=False,
            changed_event=self.populate_list
        )
        
        super().__init__(*args, **kwargs)

        self._list.get_datetimefield_options = self.get_datetimefield_options

    def get_queryset(self, request, qs):

        if self._recently_updated.value:
            qs = qs.recently_updated()

        return qs

    def get_toolbar_buttons(self, has_add_permission=False):
        return ('_add_btn' if has_add_permission else None, '_recently_updated')


    def get_datetimefield_options(self, column_name):

        now             = timezone.now()
        today_begin     = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end       = now.replace(hour=23, minute=59, second=59, microsecond=999)
        next_4_months   = today_end + timedelta(days=4*30)

        month_begin     = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        month_end       = now.replace(day=monthrange(now.year, now.month)[1], hour=23, minute=59, second=59, microsecond=999)

        return {
            'items': [
                ("{0}__gte={1}&{0}__lte={2}".format(column_name, today_begin.isoformat(), today_end.isoformat()),      'Today'),
                ("{0}__gte={1}&{0}__lte={2}".format(column_name, month_begin.isoformat(), month_end.isoformat()),      'This month'),
                ("{0}__gte={1}&{0}__lte={2}".format(column_name, today_begin.isoformat(), next_4_months.isoformat()),  'Next 4 months'),
                ("{0}__month=1".format(column_name), 'Jan'),
                ("{0}__month=2".format(column_name), 'Fev'),
                ("{0}__month=3".format(column_name), 'Mar'),
                ("{0}__month=4".format(column_name), 'Apr'),
                ("{0}__month=5".format(column_name), 'May'),
                ("{0}__month=6".format(column_name), 'Jun'),
                ("{0}__month=7".format(column_name), 'Jul'),
                ("{0}__month=8".format(column_name), 'Ago'),
                ("{0}__month=9".format(column_name), 'Sep'),
                ("{0}__month=10".format(column_name), 'Oct'),
                ("{0}__month=11".format(column_name), 'Nov'),
                ("{0}__month=12".format(column_name), 'Dez'),
            ]
        }


    def show_edit_form(self, obj_pk):
        if obj_pk:
            self.execute_js('window.location="/app/opportunities-app/#/funding.apps.fundingopportunities.EditFundingApp/?fund_pk={0}"'.format(obj_pk))
        else:
            super(FundingOpportunitiesApp, self).show_edit_form(obj_pk)
