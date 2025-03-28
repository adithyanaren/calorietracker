import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-@4kc!tcc%1v8z^4%qe(s!aelu)ez^^$gh7#(a1*kqzm4$b7a^k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS =  ['.elasticbeanstalk.com', 'elasticbeanstalk-us-east-1-613455511581.s3.amazonaws.com','http://calorie-tracker-env-1.eba-kgu8k7sc.us-east-1.elasticbeanstalk.com/','*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tracker',
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

ROOT_URLCONF = 'calorie_tracker.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # You can add your custom template directories here
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

WSGI_APPLICATION = 'calorie_tracker.wsgi.application'


# Database
# Replacing SQLite with MySQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'calorietracker_db',       # New MySQL database name
        'USER': 'calorie_user',              # MySQL user
        'PASSWORD': 'Optimus16#',       # MySQL password (replace with your actual password)
        'HOST': 'calorietrackerdb.c1xfuusbqsaf.us-east-1.rds.amazonaws.com',                 # Database host, usually localhost
        'PORT': '3306',                      # Default MySQL port
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication redirects
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/login/'

# Email settings (using Gmail as an example)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'adithya.ak6@gmail.com'
EMAIL_HOST_PASSWORD = 'pbzepxkbdtdsnsyc'  # Use an App Password if using Gmail
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

AWS_REGION = "us-east-1"  # Change if needed
AWS_SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:613455511581:mealalert"

# AWS SQS Configuration
AWS_SQS_QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/613455511581/MealLoggingQueue"
AWS_SQS_QUEUE_ARN = "arn:aws:sqs:us-east-1:613455511581:MealLoggingQueue"
AWS_REGION = "us-east-1"

