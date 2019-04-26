# Core funding opportunities

## How to install

Install the application with the pip:

    > pip install core-funding
    
Create a django project and set the next configurations:

```python

INSTALLED_APPS = [
    'funding',
    ...
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'funding_settings.wsgi.application'

STATICFILES_DIRS = [
    ...
    os.path.join(BASE_DIR, "static", 'css'),
    os.path.join(BASE_DIR, "static", 'img'),
]


PERMISSION_EDIT_FUNDING = 'PROFILE: Can edit the funding opportunities'

FUNDING_OPPORTUNITIES_EMAIL_SUBJECT = 'FUNDING OPPORTUNITIES | UPDATED {datetime}'
FUNDING_OPPORTUNITIES_EMAIL_TO      = 'ricardo.ribeiro@research.fchampalimaud.org'

EMAIL_FROM          = 'no.reply@research.fchampalimaud.org'
EMAIL_HOST          = ''
EMAIL_HOST_USER     = 'no.reply@research.fchampalimaud.org'
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT          = 0
EMAIL_USE_TLS       = True


#############################################
# Newsletter settings
# =============================================================================

# show new funding opportunities with
NEW_FUNDS_N_DAYS = 5*30  

# number of days required for a fund to be considered a closing fund.
CLOSING_FUNDS_N_DAYS = 30  

# Maximum of funds to send
NEW_FUNDS_N_MAX = 8

ROLLING_FUNDS_MONTHS = [3, 6, 9]
```

Set the django projects urls.py


```python

...

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'osp/', include('funding.urls')),
]

...

```

Execute the command:

    python manage.py migrate


	
## Printscreens

    App to edit the funding opportunities

![Fundings list](https://raw.githubusercontent.com/fchampalimaud/core-funding/master/docs/images/fundings-list.png)

![Edit a funding opportunity](https://raw.githubusercontent.com/fchampalimaud/core-funding/master/docs/images/funding-edit.png)


    Timeline app to visualise the next funding opportunities per date
	
![Timeline](https://raw.githubusercontent.com/fchampalimaud/core-funding/master/docs/images/timeline.png)

![Funding popup](https://raw.githubusercontent.com/fchampalimaud/core-funding/master/docs/images/funding-popup.png)

    Each user can set his prefered topics, which will provide important information to the pre award team.

![Profile](https://raw.githubusercontent.com/fchampalimaud/core-funding/master/docs/images/profile.png)	

![Funding stats](https://raw.githubusercontent.com/fchampalimaud/core-funding/master/docs/images/fundings-stats.png)

       The newsletter can be pre-visualized and sent in the newsletter app

![Newsletter](https://raw.githubusercontent.com/fchampalimaud/core-funding/master/docs/images/newsletter.png)

