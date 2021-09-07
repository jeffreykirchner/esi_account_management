from django.contrib import admin
from django.contrib.auth.models import User

from main.models import Parameters
from main.models import Profile


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
    fields = ('user', 'organization', 'profile_id')
    readonly_fields = ['profile_id']
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

