'''
build main.views.registration
'''
from django.core.exceptions import ImproperlyConfigured
from .login_view import *
from .logout_view import *
from .create_account import *
from .verify_account import *
from .verify_account_resend import *
from .account import *
