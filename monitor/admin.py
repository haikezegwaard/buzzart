from django.contrib import admin
from monitor.models import Project, Summary, InterestProject, BuzzartUpdate
from monitor.models import Account

# Register your models here.
admin.site.register(Project)
admin.site.register(Summary)
admin.site.register(InterestProject)
admin.site.register(BuzzartUpdate)
admin.site.register(Account)
