from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Message

# Simple User Admin
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('username', 'email')

# Simple Message Admin
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'timestamp')
    actions = ['delete_selected']
    
    def delete_selected(self, request, queryset):
        queryset.delete()
    delete_selected.short_description = "Delete selected messages"

admin.site.register(User, CustomUserAdmin)
admin.site.register(Message, MessageAdmin)
