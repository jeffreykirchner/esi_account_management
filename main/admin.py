from django.contrib import admin

from main.models import Parameters, experiments
from main.models import People
from main.models import Experiments

from main.forms import PeopleAdminForm

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

class PeopleAdmin(admin.ModelAdmin):
    '''
    People model admin
    '''
    form = PeopleAdminForm

    fields = ('first_name', 'last_name', 'email', 'organization', 'user_name', 'experiments')
    readonly_fields = ['user_name']
    list_display = ['last_name', 'first_name', 'email', 'organization']

    actions = []

admin.site.register(People, PeopleAdmin)

class ExperimentsAdmin(admin.ModelAdmin):
    '''
    Experiments model admin
    '''

    actions = []

admin.site.register(Experiments, ExperimentsAdmin)

