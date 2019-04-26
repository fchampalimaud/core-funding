from funding.models import OpportunityTopic, Profile

from pyforms.basewidget import BaseWidget, segment, no_columns
from pyforms_web.web.middleware import PyFormsMiddleware

from pyforms.controls import ControlList
from pyforms.controls import ControlCombo

from django.conf import settings
from confapp import conf
import locale

class TopicsStats(BaseWidget):

    UID = 'topics-stats-app'

    TITLE = 'Topics stats'
    LAYOUT_POSITION = conf.ORQUESTRA_HOME

    ORQUESTRA_MENU       = 'left'
    ORQUESTRA_MENU_ORDER = 10
    ORQUESTRA_MENU_ICON  = 'chart bar outline'

    AUTHORIZED_GROUPS    = [settings.PERMISSION_EDIT_FUNDING, 'superuser']

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._order = ControlCombo('Order by', label_visible=False, changed_event=self.__load_stats)
        self._table = ControlList('Topics statistics', 
            horizontal_headers=['Topic', 'Users', 'Funds', 'Total funds', 'Average per fund'])

        #self._order.add_item('Topics', 0)
        self._order.add_item('Users', 1)
        self._order.add_item('Funds', 2)
        self._order.add_item('Total funds', 3)
        self._order.add_item('Average per fund', 4)

        self.formset = [
            '_order',
            '_table'
        ]

        self._order.value = 1
        self.__load_stats()

    def __load_stats(self):
        OpportunityTopic.objects.filter()

        locale.setlocale( locale.LC_ALL, '' )

        q = OpportunityTopic.objects.all()
        
        values = []
        for topic in q:
            count_funds = topic.count_funds()
            total_funds = topic.total_funds()
            values.append( [
                topic.opportunitytopic_name,
                topic.count_users(),
                count_funds,
                total_funds,
                total_funds/count_funds if count_funds>0 else 0
            ] )

        index = int(self._order.value)
        values = sorted(values, key=lambda x: -x[index])

        values = [(v1,v2 if v2>0 else '',v3 if v3>0 else '','€ {:,.2f}'.format(v4) if v4>0 else '', '€ {:,.2f}'.format(v5) if v5>0 else '' ) for v1,v2,v3,v4,v5 in values]
        
        self._table.value = values
