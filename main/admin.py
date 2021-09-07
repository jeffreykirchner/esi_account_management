from django.contrib import admin
from django.contrib.auth.models import User

from main.models import Parameters
from main.models import Profile
from main.models import Experiments

from main.forms import ProfileAdminForm


# Register your models here.

class ParametersAdmin(admin.ModelAdmin):
    '''
    Parameters model admin
    '''
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    actions = []

admin.site.register(Parameters, ParametersAdmin)

class ProfileAdmin(admin.ModelAdmin):
    '''
    People model admin
    '''
    form = ProfileAdminForm

    fields = ('user', 'global_id', 'organization', 'experiments')
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

    actions = []

admin.site.register(Experiments, ExperimentsAdmin)

