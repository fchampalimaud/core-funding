from funding.models import FundingOpportunity, OpportunityTopic, OpportunitySubject, UserFilters, Profile
from pyforms_web.web.middleware import PyFormsMiddleware

from django.utils     import timezone
from datetime         import timedelta
from django.db.models import Q

from pyforms.basewidget import BaseWidget, no_columns
from pyforms.controls import ControlButton
from pyforms.controls import ControlTemplate
from pyforms.controls import ControlMultipleSelection
from .viewfund import ViewFundApp

from confapp import conf

class TimelineApp(BaseWidget):
    
    UID = 'timeline-app'
    
    TITLE = 'Timeline'    
    LAYOUT_POSITION = conf.ORQUESTRA_HOME

    ORQUESTRA_MENU       = 'left'
    ORQUESTRA_MENU_ORDER = 0
    ORQUESTRA_MENU_ICON  = 'time'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._topics      = ControlMultipleSelection('Topics')
        self._subjects    = ControlMultipleSelection('Subjects')
        self._refresh_btn = ControlButton('<i class="filter icon"></i> Filter', default=self.render_html, label_visible=False)
        self._mytopics_btn= ControlButton('<i class="plus icon"></i><i class="certificate icon"></i> Add my topics', default=self.__add_mytopics, css='basic', label_visible=False)
        self._htmlcontrol = ControlTemplate('Timeline', template='timeline/funding-opportunities.html')

        self.formset = [
            ('_topics','_subjects'),
            no_columns('_mytopics_btn', '_refresh_btn'),
            '_htmlcontrol'
        ]

        self.__load_topics()
        self.__load_subjects()
        
        self.render_html(False)

        request = PyFormsMiddleware.get_request()
        self.fund_id = request.GET.get('fund', None)

    def __add_mytopics(self):
        user    = PyFormsMiddleware.user()
        profile = Profile.objects.get(user=user)
        topics  = list(self._topics.value)

        for topic in profile.topics.all():
            topics.append( str(topic.pk) )
        
        self._topics.value = topics
        
    def __load_topics(self):
        topics = OpportunityTopic.objects.all().order_by('opportunitytopic_name')
        for topic in topics:
            count = topic.count_funds()
            if count==0: continue
            self._topics.add_item(
                "{0} ({1})".format(topic.opportunitytopic_name, count), 
                topic.pk
            )

    def __load_subjects(self):
        subjects = OpportunitySubject.objects.all().order_by('opportunitysubject_name')
        for subject in subjects:
            count = subject.count_funds()
            if count==0: continue
            self._subjects.add_item(
                "{0} ({1})".format(subject.opportunitysubject_name, count), 
                subject.pk
            )


    def init_form(self, parent=None):
        if self.fund_id: self.open_funding(self.fund_id)
        return super(TimelineApp,self).init_form(parent)

    def open_funding(self, pk=None):
        fund_id = self._htmlcontrol.action_param if pk is None else pk
        a = ViewFundApp(fund_id)
        a._uid = fund_id

    def render_html(self, register_filter=True):
        subjects = OpportunitySubject.objects.all().order_by('opportunitysubject_name')
        topics   = self._topics.value
        subjects = self._subjects.value

        today = timezone.now()
        
        if register_filter:
            reg = UserFilters(user=PyFormsMiddleware.user())
            reg.save()
            reg.topics.add(*list(OpportunityTopic.objects.filter(pk__in=topics)))
            reg.subjects.add(*list(OpportunitySubject.objects.filter(pk__in=subjects)))
            

        funds = FundingOpportunity.objects.filter( 
            Q(fundingopportunity_end__gte=today) | Q(fundingopportunity_loideadline__gte=today) 
        )

        if len(topics)>0:
            funds = funds.filter(topics__in=topics)
        if len(subjects)>0:
            funds = funds.filter(subject__in=subjects)
        
        funds = funds.order_by('fundingopportunity_end')
        user = PyFormsMiddleware.user
        
        res = []
        for fund in funds:
            classes = []
            #if fund.groups.filter(group=groups).exists(): classes.append('mine')
            classes.append( 'subject'+str(fund.subject.pk) )
            
            two_weeks_ago = timezone.now() + timedelta(days=-14) 
            if fund.fundingopportunity_createdon>=two_weeks_ago: classes.append('new')

            date, display_date, enddate = 0, None, None
            if fund.fundingopportunity_end:
                date         = fund.fundingopportunity_end.isoformat()
                display_date = fund.fundingopportunity_end.strftime("%d. %B")
                enddate      = fund.fundingopportunity_end.strftime("%d. %B %Y")
            elif fund.fundingopportunity_loideadline:
                date         = fund.fundingopportunity_loideadline.isoformat()
                display_date = fund.fundingopportunity_loideadline.strftime("%d. %B")
                enddate      = fund.fundingopportunity_loideadline.strftime("%d. %B %Y")

            obj = { 
                'classes':      ' '.join(classes),
                "pk":           fund.pk,
                "title":        fund.fundingopportunity_name,
                "date":         date,
                "display_date": display_date,
                "enddate":      enddate,
                "grantor":      fund.financingAgency.grantor_name,
                "subject":      fund.subject.opportunitysubject_name,
                "body":         fund.fundingopportunity_brifdesc,
                "read_more":    fund.fundingopportunity_link,
                "topics":       fund.topics.all(),
            }
            
            #if fund.financingAgency.grantor_icon: obj['photo_url'] = "/media/{0}".format( fund.financingAgency.grantor_icon )
            res.append(obj)


        self._htmlcontrol.value = {'subjects': subjects, 'nodes': sorted(res, key=lambda x: x['date'])} 