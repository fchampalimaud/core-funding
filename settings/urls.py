from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from supplier.views import *
from supplier import views
from humanresources import views
from communications.views import close_communication

admin.autodiscover()


urlpatterns = patterns('',

	url(r'^humanresources/viewprofiles/$', views.list_users_by_group),
	url(r'^osp/fundingopportunities-timeline/$', 'osp.views.fundingOpportunitiesTimeline'),
	url(r'^osp/fundingopportunities-timeline/ajax/$', 'osp.views.fundingOpportunities'),
	url(r'^osp/fundingopportunity/(?P<pk>\d+)/copy/$', 'osp.views.copyFundingOpportunity'),
	

	
	url(r'^communication/close/(?P<comid>\d+)/$', close_communication, name='close_communication'),
	# Examples:
	# url(r'^$', 'cnp_core.views.home', name='home'),
	# url(r'^blog/', include('blog.urls')),
	#url(r'^supplier/upload-form/$', views.upload_form),
	url(r'^humanresources/contractproposal/approve/(?P<contractproposal_id>\d+)/$', 'humanresources.views.approve_contract', name='approve_contract'),
	url(r'^humanresources/contractproposal/close/(?P<contractproposal_id>\d+)/$', 'humanresources.views.close_contract', name='close_contract'),
	url(r'^humanresources/contractproposal/print/(?P<contractproposal_id>\d+)/$', 'humanresources.views.print_contract', name='print_contract'),



	url(r'^supplier/supplier/budgetslist/$', 'supplier.views.budgetslist', name='budgetslist'),

	url(r'^supplier/budgetslist/supplier/importbudgets/(?P<docname>)/$', 'supplier.views.budgetslist', name='budgetslist'),
	url(r'^supplier/importbudgets/(?P<docname>\d+)/$', 'supplier.views.importbudgets', name='importbudgets'),
	url(r'^supplier/importbudgets/(?P<docname>)/$', 'supplier.views.importbudgets', name='importbudgets'),
	#url(r'^supplier/index/$', 'supplier.views.index', name='index'),

	url(r'^export/orders_from_project/(?P<project_id>\d+)/$', 'supplier.views.orders_from_project'),

	url(r'^report/$', 'supplier.views.downloadReport'),
	url(r'^accounts/', include('allauth.urls')),
	url(r'^reports/report/(?P<report_id>\d+)', 'reports.views.viewReport' ),
	url(r'^reports', 'reports.views.listReports' ),

	url(r'^report_builder/', include('report_builder.urls')),
	url(r'^', include(admin.site.urls)),
)


if settings.DEBUG:
	urlpatterns = patterns('',
	url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
		{'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
	url(r'', include('django.contrib.staticfiles.urls')),
) + urlpatterns

