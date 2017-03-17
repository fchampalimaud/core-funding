from django.apps import AppConfig

class FundingNewsletterConfig(AppConfig):
	name = 'funding_newsletter'
	verbose_name = "Funding newsletter"

	orquestra_plugins = [
		'funding_newsletter.pyforms_apps.newsletter_previsualisation.NewsletterPrevisualisation',
	]