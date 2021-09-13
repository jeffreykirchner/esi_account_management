from django.db.models import CharField, F, Value

from main.models import HelpDocs

class HelpDocsMixin:
    '''
    help documentation mixin
    '''

    def get_help_text(self, path):
        '''
        return the help documentation for the specified path
        '''

        try:
            help_text = HelpDocs.objects.annotate(rp = Value(path, output_field=CharField()))\
                                        .filter(rp__icontains=F('path')).first().text

        except Exception  as e:
            help_text = "No help doc was found."

        return help_text
