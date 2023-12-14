import os
import sys
from pathlib import Path
import cloudinary
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

map(lambda directory: sys.path.insert(0, os.path.join(BASE_DIR, directory)), ['apps'])

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-32l(g+x+d^g9h461bvl86!32=$r^k0eyxmd*270=bj*67ei+0u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool, default=False)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])

# Application definition

DJANGO_APPS = [
    'jet_sidebar',
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]

MY_APPS = [
    'users',
    'website',
    'competitor',
    'financial',
    'competition',
    'news',
    'flat_pages',
    'image_bank',
]

THIRD_APPS = [
    'ckeditor',
    'ckeditor_uploader',
    'easy_thumbnails',
    'easy_thumbnails.optimize',
    'widget_tweaks',
    'corsheaders',
    'django_registration',
    'rest_framework',
    'tinymce',
    'logentry_admin',
    'cloudinary',
    'import_export'

]

INSTALLED_APPS = DJANGO_APPS + MY_APPS + THIRD_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'radical.urls'

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
                'website.context_processors.config',
                'website.context_processors.menu_pages',
                'website.context_processors.menu_news',
                'website.context_processors.current_edition',
            ],
        },
    },
]

WSGI_APPLICATION = 'radical.wsgi.application'
LOGIN_URL = '/'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# if True:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME', default='piocera'),
        'USER': config('DB_USER', default=''),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default=''),
        # 'CONN_MAX_AGE': 600,  # segundos
    }
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

SITE_ID = 1

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Fortaleza'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

X_FRAME_OPTIONS = 'SAMEORIGIN'

MEDIA_ROOT = config('MEDIA_ROOT')
MEDIA_URL = '/media/'

STATIC_ROOT = config('STATIC_ROOT')

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# STORAGES = {
#     "staticfiles": {
#         "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
#     },
# }

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

# Todo: Somente enquanto tiver django adm
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_UPLOAD_SLUGIFY_FILENAME = True
CKEDITOR_BROWSE_SHOW_DIRS = True

CKEDITOR_CONFIGS = {
    'basic': {
        'toolbar': [
            ['Source', '-', 'Bold', 'Italic', 'Underline', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', '-',
             'RemoveFormat', 'Update', '-', 'Link', 'Unlink', 'TextColor', 'FontSize', '-', 'Find', 'Replace', '-',
             'Image', 'Table', 'Iframe', 'Youtube', 'Html5audio', 'Embed', 'EmbedCodeNative'],
        ],
        'forcePasteAsPlainText': True,
        'entities': False,
        'htmlEncodeOutput': False,
        'allowedContent': True,
        'fillEmptyBlocks': False,
        'extraPlugins': 'youtube,html5audio,embed,embedcodenative,imageuploader',
        'width': '100%',
        'contentsCss': ('/static/ckeditor/content.css', '/static/ckeditor/ckeditor/contents.css'),
    },
    'disable': {
        'toolbar': [],
        'width': '600px',
        'toolbarCanCollapse': False,
        'readOnly': True,
    },

}

TINYMCE_DEFAULT_CONFIG = {
    'plugins': "table,spellchecker,paste,searchreplace,image,link,media,code,insertdatetime,nonbreaking,contextmenu,visualchars",
    # 'width': "100%",
    'height': "400px",
    "file_picker_callback": """function (cb, value, meta) {
        var input = document.createElement("input");
        input.setAttribute("type", "file");
        if (meta.filetype == "image") {
            input.setAttribute("accept", "image/*");
        }
        if (meta.filetype == "media") {
            input.setAttribute("accept", "video/*");
        }

        input.onchange = function () {
            var file = this.files[0];
            var reader = new FileReader();
            reader.onload = function () {
                var id = "blobid" + (new Date()).getTime();
                var blobCache = tinymce.activeEditor.editorUpload.blobCache;
                var base64 = reader.result.split(",")[1];
                var blobInfo = blobCache.create(id, file, base64);
                blobCache.add(blobInfo);
                cb(blobInfo.blobUri(), { title: file.name });
            };
            reader.readAsDataURL(file);
        };
        input.click();
    }""",
}

TINYMCE_IMAGES_UPLOAD_PATH = "uploads/"

# easy_thumbnails
THUMBNAIL_SUBDIR = 'thumbs'
THUMBNAIL_QUALITY = 90
THUMBNAIL_EXTENSION = 'webp'

# jet_sidebar
SID_TITLE_MENU = False

SID_APP_ICONS = {
    'auth': {
        'class_icon': 'fas fa-desktop',
    },
    'admin': {
        'class_icon': 'fas fa-door-closed',
    },
    'sites': {
        'class_icon': 'fas fa-globe',
    },
    'users': {
        'class_icon': 'fas fa-users',
    },
}

SID_ICON_SMALL = {
    'icon': '/images/logos/cerapioBranca.png',
    'width': '70px',
    'style': 'padding: 5px 0 5px 5px',
}

SID_ICON_LARGE = {
    'icon': '/images/logos/cerapioBranca.png',
    'width': '100px',
    'style': 'padding: 5px 0 5px 15px',
}

CORS_ORIGIN_ALLOW_ALL = True

# CORS_ORIGIN_WHITELIST = config('CORS_ORIGIN_WHITELIST', cast=lambda v: [s.strip() for s in v.split(',')])
# CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', cast=lambda v: [s.strip() for s in v.split(',')])
CORS_ORIGIN_WHITELIST = [
    'https://www.piocera.com.br',
    'https://piocera.com.br',
    'https://www.cerapio.com.br',
    'https://cerapio.com.br',
    'https://stg.radicalproducoes.com.br',
]
# No env ao colocar vários dominios separar por virgula
# CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', cast=lambda v: [s.strip() for s in v.split(',')])
CSRF_TRUSTED_ORIGINS = [
    'https://www.piocera.com.br',
    'https://piocera.com.br',
    'https://www.cerapio.com.br',
    'https://cerapio.com.br',
    'https://stg.radicalproducoes.com.br',
]


LOGIN_REDIRECT_URL = '/'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# DEFAULT_FROM_EMAIL = 'Radical360 <eduardo.silva@somosicev.com>'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'eduardo.silva@somosicev.com'
# EMAIL_HOST_PASSWORD = 'somosicev060'
# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False
# EMAIL_PORT = 587
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'Radical360 <piocera@fabricadegenios.com.br>'
EMAIL_HOST = 'smtp.hostinger.com'
EMAIL_HOST_USER = 'piocera@fabricadegenios.com.br'
EMAIL_HOST_PASSWORD = 'Piocera123@'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_PORT = 587

# DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
# EMAIL_HOST = config('EMAIL_HOST')
# EMAIL_HOST_USER = config('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
# EMAIL_USE_TLS = config('EMAIL_USE_TLS')
# EMAIL_PORT = config('EMAIL_PORT')

if config('ASAAS_DEBUG', cast=bool, default=True):
    # asaas temporário
    ASAAS_API_URL = 'https://sandbox.asaas.com/api/v3'
    HEADERS = {
        'access_token': config('ASAAS_TOKEN_DEV')

    }
else:
    ASAAS_API_URL = 'https://www.asaas.com/api/v3'
    HEADERS = {
        'access_token': config('ASAAS_TOKEN_PROD')
    }

cloudinary.config(
    cloud_name=config('CLOUD_NAME'),
    api_key=config('API_KEY'),
    api_secret=config('API_SECRET')
)
DATA_UPLOAD_MAX_NUMBER_FILES = 2000
# Define o tamanho máximo para 200 MB (200 * 1024 * 1024 bytes)
DATA_UPLOAD_MAX_MEMORY_SIZE = 209715200