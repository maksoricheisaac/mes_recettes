"""
URLs pour l'application recipes
"""
from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    # Liste et détail des recettes
    path('', views.recipe_list, name='list'),
    path('recipe/<slug:slug>/', views.recipe_detail, name='detail'),
    
    # CRUD recettes
    path('create/', views.recipe_create, name='create'),
    path('recipe/<slug:slug>/edit/', views.recipe_edit, name='edit'),
    path('recipe/<slug:slug>/delete/', views.recipe_delete, name='delete'),
    
    # Actions AJAX
    path('recipe/<slug:slug>/like/', views.recipe_like, name='like'),
    path('recipe/<slug:slug>/favorite/', views.recipe_favorite, name='favorite'),
    
    # Commentaires
    path('recipe/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    
    # Catégories
    path('category/<slug:slug>/', views.category_recipes, name='category'),
]