from django.contrib import admin

from mailer.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_email',)
    list_filter = ('client_name',)
    search_fields = ('client_name',)
