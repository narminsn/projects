from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Team)
admin.site.register(TeamMembers)
admin.site.register(TokenModelTeam)
admin.site.register(TeamDocuments)
