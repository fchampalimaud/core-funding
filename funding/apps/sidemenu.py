from pyforms_web.web.middleware import PyFormsMiddleware
from pyforms.basewidget import BaseWidget
from pyforms.controls   import ControlTemplate

from funding.models import Favorite

class SideMenuApp(BaseWidget):
	
	UID = 'sidemenu-app'

	TITLE = 'Favorites'
	LAYOUT_POSITION = 'side-menu-app-place'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self._htmlcontrol = ControlTemplate('Side menu', template='sidemenu-app.html')

		self.formset = ['_htmlcontrol']
		self.reload()
		

	def reload(self):
		user = PyFormsMiddleware.user()
		favorites = Favorite.objects.filter(user=user, active=True).order_by('funding__fundingopportunity_name')
		self._htmlcontrol.value = {'favorites': favorites}