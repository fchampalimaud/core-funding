import sys,os; 
sys.path.append("/Users/carlos/Dropbox/Projects/champalimaud/research_core/"); 
sys.path.append("/Users/carlos/Dropbox/Projects/champalimaud/research_core/research-core"); 
os.chdir("/Users/carlos/Dropbox/Projects/champalimaud/research_core/research-core")
print(os.getcwd())
#print(os.listdir("."))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cnp_core_conf.settings")

from osp.models 			import *
from django.conf 			import settings
from django.utils 			import timezone
from django.contrib.auth 	import models
from django.core.mail 		import EmailMessage
from django.template.loader import render_to_string


funds = FundingOpportunity.objects.filter(fundingopportunity_end__gte=timezone.now()).order_by('fundingopportunity_start')

print(funds)

#rendered = "This report was sent to:<br/><br/>"+'<br/>'.join( sent_to_users )
#msg = EmailMessage('Contracts expiring in the next %d days: sending report' %  settings.ENDING_CONTRACT_WARNING_N_DAYS_BEFORE, 
	#rendered, settings.ENDING_CONTRACT_FROM, SEND_TO)
#msg.content_subtype = "html"
#msg.send()
#sent_to_users.append(user)