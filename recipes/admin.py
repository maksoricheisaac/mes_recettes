"""
Configuration admin pour l'application recipes
"""
from django.contrib import admin
from .models import Recipe, Category, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'difficulty', 'is_published', 'created_at')
    list_filter = ('category', 'difficulty', 'is_published', 'created_at')
    search_fields = ('title', 'description', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('likes', 'favorites')
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('title', 'slug', 'description', 'author', 'category', 'image')
        }),
        ('Détails de la recette', {
            'fields': ('ingredients', 'instructions', 'prep_time', 'cook_time', 'servings', 'difficulty')
        }),
        ('Statut', {
            'fields': ('is_published', 'is_featured')
        }),
        ('Interactions', {
            'fields': ('likes', 'favorites'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'author', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('recipe__title', 'author__username', 'content')
    readonly_fields = ('created_at', 'updated_at')
    
    actions = ['approve_comments', 'disapprove_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = "Approuver les commentaires sélectionnés"
    
    def disapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)
    disapprove_comments.short_description = "Désapprouver les commentaires sélectionnés"