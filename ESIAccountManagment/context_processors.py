'''
context processors
'''
from django.conf import settings # import the settings file

def get_debug(request):
    '''
    return debug settings to templates
    '''
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'DEBUG': settings.DEBUG}