'''
log out user
'''
import logging

from django.contrib.auth import logout
from django.shortcuts import render
from django.views.generic import TemplateView

from main.views import HelpDocsMixin

class LogoutView(HelpDocsMixin, TemplateView):
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

        return render(request, self.template_name, {'help_text' : self.get_help_text(request.path),})

    
