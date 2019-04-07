from django.contrib import admin
from sandbox.example.models import *


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    pass
