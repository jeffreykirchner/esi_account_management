'''
log out user
'''
import logging

from django.contrib.auth import logout
from django.shortcuts import render
from django.views.generic import TemplateView

class LogoutView(TemplateView):
    '''
     log out class view
    '''

    template_name = 'registration/logged_out.html'

    def get(self, request, *args, **kwargs):
        '''
        handle get requests
        '''
        logger = logging.getLogger(__name__)     
        logger.info(f"Log out {request.user}")

        logout(request)

        return render(request, self.template_name, {})

    
