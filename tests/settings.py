import dj_database_url

DATABASES = {
    'default': dj_database_url.parse('mysql://root:root@mysql/pursed')
}


SECRET_KEY = 'fake-key'

INSTALLED_APPS = ('django.contrib.auth',
                  'django.contrib.contenttypes',
                  'django.contrib.sessions',
                  'django.contrib.admin',
                  'django.contrib.sites',
                  'wallet',
                  'tests', )

AUTH_USER_MODEL = 'auth.User'
