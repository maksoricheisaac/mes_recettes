"""
Configuration admin pour l'application accounts
"""
from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'created_at', 'recipes_count')
    list_filter = ('created_at', 'location')
    search_fields = ('user__username', 'user__email', 'bio')
    readonly_fields = ('created_at', 'updated_at')
    
    def recipes_count(self, obj):
        return obj.recipes_count
    recipes_count.short_description = 'Nombre de recettes'