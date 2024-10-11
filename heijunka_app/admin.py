from django.contrib import admin
from .models import Site, Client, TypeClient, Schedule


admin.site.register(Site)
admin.site.register(Client)
admin.site.register(TypeClient)
admin.site.register(Schedule)
