from funding.models import FundingOpportunity, Favorite

from pyforms_web.web.middleware import PyFormsMiddleware
from pyforms_web.widgets.django import ModelViewFormWidget

from pyforms.basewidget import no_columns, segment
from pyforms.controls import ControlButton

from django.conf import settings
from confapp import conf

class ViewFundApp(ModelViewFormWidget):
	
	UID 			= 'viewfund-app'
	
	TITLE 				 = 'Funding opportunities'
	ORQUESTRA_MENU  	 = 'left'
	ORQUESTRA_MENU_ORDER = 0
	ORQUESTRA_MENU_ICON  = 'money'
	LAYOUT_POSITION   	 = conf.ORQUESTRA_NEW_WINDOW

	MODEL     = FundingOpportunity
	FIELDSETS = [
		no_columns('_favoritebtn','_urlbtn','_editbtn'),
		'h2:Opportunity details',
		segment([ 
			('subject','fundingopportunity_link'),
			('fundingopportunity_name','fundingopportunity_end'),
			('fundingopportunity_loideadline', 'fundingopportunity_fullproposal'),
			'topics',
		]),
		'h2:Financing info',
		segment([
			'financingAgency',
			('fundingopportunity_value','currency','paymentfrequency', 'fundingopportunity_duration'),			
		]),
		'h2:Description',
		segment([
			'fundingopportunity_eligibility',
			'fundingopportunity_scope',
			'fundingopportunity_brifdesc',
		])
	]


	ADD_FAVORITE_LABEL 		= '<i class="icon star" ></i> Add to favorites'	
	REMOVE_FAVORITE_LABEL 	= '<i class="icon empty star" ></i> Remove from favorites'

	def __init__(self, obj_pk):
		self.obj = FundingOpportunity.objects.get(pk=obj_pk)
		ModelViewFormWidget.__init__(self, title=self.obj.fundingopportunity_name, pk=obj_pk)

		if self.fundingopportunity_loideadline.value is None:
			self.fundingopportunity_loideadline.hide()
			
		if self.fundingopportunity_fullproposal.value is None:
			self.fundingopportunity_fullproposal.hide()

		user = PyFormsMiddleware.user()
		

		self._editbtn = ControlButton('<i class="icon edit" ></i> Edit', label_visible=False)
		
		self._editbtn.value = 'window.location = "/app/opportunities-app/#/funding.apps.fundingopportunities.EditFundingApp/?fund_pk={0}";'.format(obj_pk)
		if not user.groups.filter(name__in=[settings.PERMISSION_EDIT_FUNDING]).exists():
			self._editbtn.hide()
		
		self._favoritebtn = ControlButton('Favorite')
		self._favoritebtn.label_visible = False
		self._favoritebtn.value = self.__mark_as_favorite

		if Favorite.objects.filter(user=user, funding=self.obj, active=True).exists():
			self._favoritebtn.label = self.REMOVE_FAVORITE_LABEL
			self._favoritebtn.css = 'primary basic'
		else:
			self._favoritebtn.label = self.ADD_FAVORITE_LABEL
			self._favoritebtn.css = 'blue'

		self._urlbtn = ControlButton("<i class='ui icon external'></i> URL")
		self._urlbtn.label_visible = False
		self._urlbtn.css = 'basic blue'
		if self.obj and self.obj.fundingopportunity_link:
			self._urlbtn.value = "window.open('{0}', '_blank');".format(self.obj.fundingopportunity_link)
		else:
			self._urlbtn.hide()



	def __mark_as_favorite(self):
		user = PyFormsMiddleware.user()

		favorite = None

		try:
			favorite = Favorite.objects.get(user=user,funding=self.obj)
			
			if favorite.active:
				self._favoritebtn.label = self.ADD_FAVORITE_LABEL
				self._favoritebtn.css = 'blue'
				favorite.active=False
				favorite.save()
			else:
				self._favoritebtn.label = self.REMOVE_FAVORITE_LABEL
				self._favoritebtn.css = 'primary basic'
				favorite.active=True
				favorite.save()

		except Favorite.DoesNotExist:
			Favorite(user=user, funding=self.obj, active=True).save()
			self._favoritebtn.label = self.REMOVE_FAVORITE_LABEL
			self._favoritebtn.css 	= 'primary basic'

		sidemenu_app = PyFormsMiddleware.get_instance('sidemenu-app')
		sidemenu_app.reload()