from iseteam.settings import *
import dj_database_url
DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {'default':
                   dj_database_url.config(
                  default='postgres://wesaqcqdkycbqp:SuyLbZne6yoAQAtWIDNRwWRoG5@ec2-23-23-81-221.compute-1.amazonaws.com:5432/d6mpu8c00tulqs')
        }

#IseTeamDev Facebook Settings
FACEBOOK_APP_ID = '825938124180584'
FACEBOOK_APP_SECRET = '3eeeb5be7561be905a1b8bdc45e97346' 

SITE_URL = 'http://localhost:8000'

STRIPE_LIVE_SECRET = 'sk_test_AhGjXeOolGO1EIFOrJyqjoal'
STRIPE_LIVE_PUBLISHABLE = 'pk_test_28jhCdG0CjPtgQ6E2L26AEkd'



