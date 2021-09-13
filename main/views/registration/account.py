'''
account view
'''
import logging
import json

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.db.models import CharField, F, Value
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from main.models import help_docs
from main.forms import EditAccountForm
from main.globals import profile_create_send_email

from main.views import HelpDocsMixin

class AccountView(HelpDocsMixin, TemplateView):
    '''
    account class view
    '''
    template_name = 'registration/account.html'

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        '''
        handle post requests
        '''
        data = json.loads(request.body.decode('utf-8'))

        #check for correct action
        action = data.get("action", "fail")

        if action == "update":
            return update_profile(request.user, data)

        #valid action not found        
        return JsonResponse({"status" :  "error"}, safe=False)

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        '''
        handle get requests
        '''

        form = EditAccountForm(
            initial={'first_name': request.user.first_name,
                     'last_name': request.user.last_name,
                     'email':request.user.email,
                     'organization':request.user.profile.organization}
        )

        form['email'].label = "Email (Verification required)"
        form['password1'].label = "Password (Leave blank if no change)"

        try:
            help_text = help_docs.objects.annotate(rp = Value(request.path, output_field=CharField()))\
                                        .filter(rp__icontains=F('path')).first().text

        except Exception  as e:
            help_text = "No help doc was found."

        form_ids = []
        for i in form:
            form_ids.append(i.html_name)

        return render(request, self.template_name, {'form': form,
                                                    'form_ids': form_ids,
                                                    'help_text' : self.get_help_text(request.path),})
def update_profile(user, data):
    '''
    update user's profile
    '''
    logger = logging.getLogger(__name__)
    logger.info(f"Update Profile: {user}")
    #logger.info(data)

    form_data_dict = {}

    for field in data["formData"]:
        form_data_dict[field["name"]] = field["value"]

    form = EditAccountForm(form_data_dict, user=user)

    if form.is_valid():

        email_verification_required = False

        if user.email != form.cleaned_data['email'].lower():
            email_verification_required = True

        user.first_name = form.cleaned_data['first_name'].strip().capitalize()
        user.last_name = form.cleaned_data['last_name'].strip().capitalize()
        user.email = form.cleaned_data['email'].strip().lower()
        user.username = user.email

        user.profile.organization = form.cleaned_data['organization'].strip()

        if form.cleaned_data['password1']:
            if form.cleaned_data['password1'] != "":
                user.set_password(form.cleaned_data['password1'])

        if email_verification_required:
            user.profile.email_confirmed = "no"
            profile_create_send_email(user)

        user.save()
        user.profile.save()

        return JsonResponse({"status" : "success", "email_verification_required":email_verification_required}, safe=False)

    else:
        logger.info(f"Update profile validation error {user}")
        return JsonResponse({"status":"error", "errors":dict(form.errors.items())}, safe=False)

