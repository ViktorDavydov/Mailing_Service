from django.contrib import admin

from mailer.models import Client, SendOptions


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_email',)
    list_filter = ('client_name',)
    search_fields = ('client_name',)


@admin.register(SendOptions)
class SendOptionsAdmin(admin.ModelAdmin):
    list_display = ('send_name', 'send_time', 'send_period', 'send_status',)
    list_filter = ('send_status',)
    search_fields = ('send_status',)
