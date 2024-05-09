import logging
import datetime

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.translation import ngettext
from django.db.models.functions import Lower
from django.db.backends.postgresql.psycopg_any import DateTimeTZRange
from django.utils import timezone

from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from main.models import Parameters
from main.models import Profile
from main.models import Experiments
from main.models import HelpDocs
from main.models import FrontPageNotice
from main.models import ProfileLoginAttempt

from main.forms import HelpDocForm
from main.forms import ProfileAdminForm
from main.forms import ParametersAdminForm
from main.forms import FrontPageNoticeForm


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

#profile login attempt inline
class ProfileLoginAttemptInline(admin.TabularInline):
      '''
      profile login attempt inline
      '''
      def get_queryset(self, request):
            qs = super().get_queryset(request)
            
            return qs.filter(timestamp__contained_by=DateTimeTZRange(timezone.now() - datetime.timedelta(days=30), timezone.now()))
      
      def has_add_permission(self, request, obj=None):
            return False

      def has_change_permission(self, request, obj=None):
            return False

      extra = 0  
      model = ProfileLoginAttempt
      can_delete = True
      fields=('success','note')
      readonly_fields = ('timestamp',)

class ProfileAdmin(admin.ModelAdmin):
    '''
    People model admin
    '''
    form = ProfileAdminForm

    
    readonly_fields = ['user', 'global_id']
    list_display = ['__str__', 'organization']
    inlines = [ProfileLoginAttemptInline]

    actions = []

admin.site.register(Profile, ProfileAdmin)

class UserAdmin(DjangoUserAdmin):

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

class FrontPageNoticeAdmin(admin.ModelAdmin):
            
      form = FrontPageNoticeForm

      ordering = [Lower('subject_text')]

      actions = []
      list_display = ['subject_text', 'enabled']

admin.site.register(FrontPageNotice, FrontPageNoticeAdmin)
