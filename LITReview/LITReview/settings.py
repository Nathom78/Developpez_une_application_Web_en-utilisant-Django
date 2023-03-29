"""
Django settings for LITReview project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-uc)7#@b1r7(bzw+lbgg2g+^(_lh5ye+h#83eb#qohle4*-d@hf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',  # rajout de base_user pour AbstractBaseUser .base_user
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mvp',
    'authentication',
    'django_bootstrap5',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'LITReview.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR.joinpath('templates'),
            
        ],
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

WSGI_APPLICATION = 'LITReview.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME'  : BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8
        }
    },
    {
        'NAME': 'authentication.validators.ContainsLetterValidator',
    },
    {
        'NAME': 'authentication.validators.ContainsNumberValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'fr-FR'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [BASE_DIR.joinpath('locale')]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR.joinpath('static/')]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'authentication.MyUser'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'logout'

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / "sent_emails"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.joinpath(STATIC_URL, 'media/')

# Default settings
BOOTSTRAP5 = {
    
    # The complete URL to the Bootstrap CSS file
    # Note that a URL can be either a string,
    # e.g. "https://stackpath.bootstrapcdn.com/bootstrap/5.3.0/css/bootstrap.min.css",
    # or a dict like the default value below.
    "css_url": {
        "url": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css",
        "integrity": "sha384-GLhlTQ8iRABdZLl6O3oVMWSktQOp6b7In1Zl3/Jr59b6EGGoI1aFkw7cmDA6j6gD",
        "crossorigin": "anonymous",
    },
    
    # The complete URL to the Bootstrap JavaScript file
    "javascript_url": {
        "url": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js",
        "integrity": "sha384-w76AqPfDkMBDXo30jS1Sgez6pr3x5MlQ1ZAGC+nuZB+EYdgRZgiwxhTBTkF7CXvN",
        "crossorigin": "anonymous",
    },
    
    # The complete URL to the Bootstrap CSS theme file (None means no theme).
    "theme_url": None,
    
    # Put JavaScript in the HEAD section of the HTML document (only relevant if you use bootstrap5.html).
    'javascript_in_head': False,
    
    # Wrapper class for non-inline fields.
    # The default value "mb-3" is the spacing as used by Bootstrap 5 example code.
    'wrapper_class': 'mb-3',
    
    # Wrapper class for inline fields.
    # The default value is empty, as Bootstrap5 example code doesn't use a wrapper class.
    'inline_wrapper_class': '',
    
    # Label class to use in horizontal forms.
    'horizontal_label_class': 'col-sm-2',
    
    # Field class to use in horizontal forms.
    'horizontal_field_class': 'col-sm-10',
    
    # Field class used for horizontal fields withut a label.
    'horizontal_field_offset_class': 'offset-sm-2',
    
    # Set placeholder attributes to label if no placeholder is provided.
    'set_placeholder': True,
    
    # Class to indicate required field (better to set this in your Django form).
    'required_css_class': '',
    
    # Class to indicate field has one or more errors (better to set this in your Django form).
    'error_css_class': '',
    
    # Class to indicate success, meaning the field has valid input (better to set this in your Django form).
    'success_css_class': '',
    
    # Enable or disable Bootstrap 5 server side validation classes (separate from the indicator classes above).
    'server_side_validation': True,
    
    # Renderers (only set these if you have studied the source and understand the inner workings).
    'formset_renderers': {
        'default': 'django_bootstrap5.renderers.FormsetRenderer',
    },
    'form_renderers': {
        'default': 'django_bootstrap5.renderers.FormRenderer',
    },
    'field_renderers': {
        'default': 'django_bootstrap5.renderers.FieldRenderer',
    },
}
