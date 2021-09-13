import logging

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.translation import ngettext
from django.db.models.functions import Lower

from main.models import Parameters
from main.models import Profile
from main.models import Experiments
from main.models import HelpDocs

from main.forms import HelpDocForm
from main.forms import ProfileAdminForm
from main.forms import ParametersAdminForm


# Register your models here.

class ParametersAdmin(admin.ModelAdmin):
    '''
    Parameters model admin
    '''
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    form = ParametersAdminForm
    fields = ('site_URL', 'contact_email', 'email_verification_text_subject', 'email_verification_text',
              'password_reset_text_subject', 'password_reset_text')
    actions = []

admin.site.register(Parameters, ParametersAdmin)

class ProfileAdmin(admin.ModelAdmin):
    '''
    People model admin
    '''
    form = ProfileAdminForm

    fields = ('user', 'global_id', 'organization', 'email_confirmed', 'experiments')
    readonly_fields = ['user', 'global_id']
    list_display = ['__str__', 'organization']

    actions = []

admin.site.register(Profile, ProfileAdmin)

class UserAdmin(admin.ModelAdmin):

    ordering = ['-date_joined']
    search_fields = ['last_name','first_name','email']
    list_display = ['username', 'last_name', 'first_name','email','date_joined']
    actions = []

    # def has_add_permission(self, request, obj=None):
    #     return False

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

class ExperimentsAdmin(admin.ModelAdmin):
    '''
    Experiments model admin
    '''

    #set the shared status for all users to match experiment's setting
    def update_shared_status(self, request, queryset):
        logger = logging.getLogger(__name__)
        logger.info("setup_test_users")

        counter=0

        for experiment in queryset:
            if experiment.available_to_all:
                for profile in Profile.objects.all():
                    profile.experiments.add(experiment)
                    counter += 1
            else:
                for profile in Profile.objects.all():
                    profile.experiments.remove(experiment)
                    counter += 1

                
        self.message_user(request, ngettext(
                '%d user was updated.',
                '%d users were updated.',
                counter,
        ) % counter, messages.SUCCESS)
    update_shared_status.short_description = "Set accounts to shared status of selected experiments."

    actions = ['update_shared_status']

admin.site.register(Experiments, ExperimentsAdmin)

class HelpDocAdmin(admin.ModelAdmin):
            
      form = HelpDocForm

      ordering = [Lower('title')]

      actions = []
      list_display = ['title','path']

admin.site.register(HelpDocs, HelpDocAdmin)

