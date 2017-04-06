DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'},
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
