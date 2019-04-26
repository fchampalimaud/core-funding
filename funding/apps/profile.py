from pyforms_web.web.middleware import PyFormsMiddleware
from pyforms.basewidget import BaseWidget, segment, no_columns
from pyforms.controls import ControlMultipleChecks

from funding.models import OpportunityTopic, Profile

from confapp import conf


class ProfileApp(BaseWidget):

    UID = 'profile-app'

    TITLE = 'Profile'
    LAYOUT_POSITION = conf.ORQUESTRA_HOME

    ORQUESTRA_MENU       = 'left'
    ORQUESTRA_MENU_ORDER = 1
    ORQUESTRA_MENU_ICON  = 'user'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._topics = ControlMultipleChecks('My topics', mode='scrolling', changed_event=self.__topics_changed_evt, label_visible=False)

        self.formset = [
            """info:Please select the topics that interest you more.<br/>
            This information is very important to the Pre-Award team.""",
            ' ',
            '_topics'
        ]

        self.__load_topics()


    def __topics_changed_evt(self):
        user = PyFormsMiddleware.user()
        try:
            profile = Profile.objects.get(user=user)
        except:
            profile = Profile(user=user)
            profile.save()

        profile.topics.clear()
        if len(self._topics.value)>0:
            topics = OpportunityTopic.objects.filter(pk__in=self._topics.value)
            profile.topics.add(*topics)

    def __load_topics(self):
        topics = OpportunityTopic.objects.all().order_by('opportunitytopic_name')
        for topic in topics:
            self._topics.add_item(
                topic.opportunitytopic_name, 
                topic.pk
            )

        user = PyFormsMiddleware.user()
        try:
            profile = Profile.objects.get(user=user)
        except:
            profile = Profile(user=user)
            profile.save()

        self._topics.value = [t.pk for t in profile.topics.all()]
