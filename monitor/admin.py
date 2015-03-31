from django.contrib import admin
from monitor.models import Project, Summary, InterestProject, BuzzartUpdate
from monitor.models import Account
from guardian.admin import GuardedModelAdmin

# Register your models here.
admin.site.register(Project, GuardedModelAdmin)
admin.site.register(Summary)
admin.site.register(InterestProject)
admin.site.register(BuzzartUpdate)
admin.site.register(Account)
