from django.contrib import admin

from main.models import Parameters

# Register your models here.

class ParametersAdmin(admin.ModelAdmin):
    '''
    parameters model admin
    '''
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    actions = []

admin.site.register(Parameters, ParametersAdmin)
