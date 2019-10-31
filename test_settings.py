DEBUG = True

SECRET_KEY = 'fake'

INTERNAL_APPS = [
]

EXTERNAL_APPS = [
]

MY_APPS = [
    'clean_architecture_helper',
]

INSTALLED_APPS = INTERNAL_APPS + EXTERNAL_APPS + MY_APPS
