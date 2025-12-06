"""
Configuración general del agente IA
"""
import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4-turbo-preview')

# Meta/Social Media Configuration
META_ACCESS_TOKEN = os.getenv('META_ACCESS_TOKEN')
INSTAGRAM_BUSINESS_ACCOUNT_ID = os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID')
FACEBOOK_PAGE_ID = os.getenv('FACEBOOK_PAGE_ID')

# Email Configuration
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
EMAIL_FROM = os.getenv('EMAIL_FROM', 'rebirthsecred@gmail.com')
EMAIL_FROM_NAME = os.getenv('EMAIL_FROM_NAME', 'Sacred Rebirth')

# Business Information
BUSINESS_INFO = {
    'name': os.getenv('BUSINESS_NAME', 'Sacred Rebirth'),
    'website': os.getenv('BUSINESS_WEBSITE', 'https://sacred-rebirth.com'),
    'phone': os.getenv('BUSINESS_PHONE', '+52 722 512 3413'),
    'location': os.getenv('BUSINESS_LOCATION', 'Valle de Bravo, Mexico'),
    'instagram': os.getenv('INSTAGRAM_HANDLE', '@sacredrebirthvalle'),
    'facebook': os.getenv('FACEBOOK_HANDLE', 'sacredbirthretreats'),
    'email': EMAIL_FROM
}

# Content Settings
POSTS_PER_DAY = int(os.getenv('POSTS_PER_DAY', 2))
CONTENT_LANGUAGE = os.getenv('CONTENT_LANGUAGE', 'es')
TIMEZONE = os.getenv('TIMEZONE', 'America/Mexico_City')

# Email Campaign Settings
EMAIL_CAMPAIGN_FREQUENCY = os.getenv('EMAIL_CAMPAIGN_FREQUENCY', 'weekly')
MAX_EMAILS_PER_DAY = int(os.getenv('MAX_EMAILS_PER_DAY', 50))

# Scheduling
POST_TIMES = [
    '09:00',  # Morning post
    '18:00'   # Evening post
]

# Content Calendar Path
CONTENT_CALENDAR_PATH = 'data/content_calendar.json'
LEADS_DATABASE_PATH = 'data/leads.json'
