"""
Vues pour la gestion des recettes
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Q, Count
from .models import Recipe, Category, Comment
from .forms import RecipeForm, CommentForm


def recipe_list(request):
    """
    Liste des recettes avec pagination
    """
    recipes = Recipe.objects.filter(is_published=True).order_by('-created_at')
    
    paginator = Paginator(recipes, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'recipes': page_obj,
        'categories': Category.objects.all()
    }
    return render(request, 'recipes/list.html', context)


def recipe_detail(request, slug):
    """
    Détail d'une recette avec commentaires
    """
    recipe = get_object_or_404(Recipe, slug=slug, is_published=True)
    comments = recipe.comments.filter(is_approved=True).order_by('-created_at')
    
    # Vérifier si l'utilisateur a liké ou mis en favori
    user_liked = False
    user_favorited = False
    if request.user.is_authenticated:
        user_liked = recipe.likes.filter(id=request.user.id).exists()
        user_favorited = recipe.favorites.filter(id=request.user.id).exists()
    
    # Formulaire de commentaire
    comment_form = CommentForm()
    
    # Recettes suggérées (même catégorie)
    suggested_recipes = Recipe.objects.filter(
        category=recipe.category,
        is_published=True
    ).exclude(id=recipe.id)[:4]
    
    context = {
        'recipe': recipe,
        'comments': comments,
        'comment_form': comment_form,
        'user_liked': user_liked,
        'user_favorited': user_favorited,
        'suggested_recipes': suggested_recipes
    }
    return render(request, 'recipes/detail.html', context)


@login_required
def recipe_create(request):
    """
    Créer une nouvelle recette
    """
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            messages.success(request, 'Votre recette a été créée avec succès!')
            return redirect('recipes:detail', slug=recipe.slug)
    else:
        form = RecipeForm()
    
    context = {
        'form': form,
        'title': 'Créer une recette',
        'button_text': 'Créer la recette'
    }
    return render(request, 'recipes/form.html', context)


@login_required
def recipe_edit(request, slug):
    """
    Modifier une recette existante
    """
    recipe = get_object_or_404(Recipe, slug=slug, author=request.user)
    
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre recette a été modifiée avec succès!')
            return redirect('recipes:detail', slug=recipe.slug)
    else:
        form = RecipeForm(instance=recipe)
    
    context = {
        'form': form,
        'recipe': recipe,
        'title': 'Modifier la recette',
        'button_text': 'Sauvegarder les modifications'
    }
    return render(request, 'recipes/form.html', context)


@login_required
def recipe_delete(request, slug):
    """
    Supprimer une recette
    """
    recipe = get_object_or_404(Recipe, slug=slug, author=request.user)
    
    if request.method == 'POST':
        recipe.delete()
        messages.success(request, 'Votre recette a été supprimée avec succès!')
        return redirect('accounts:profile', username=request.user.username)
    
    context = {
        'recipe': recipe
    }
    return render(request, 'recipes/delete.html', context)


@login_required
@require_POST
def recipe_like(request, slug):
    """
    Aimer/ne plus aimer une recette (AJAX)
    """
    recipe = get_object_or_404(Recipe, slug=slug, is_published=True)
    
    if recipe.likes.filter(id=request.user.id).exists():
        recipe.likes.remove(request.user)
        liked = False
    else:
        recipe.likes.add(request.user)
        liked = True
    
    return JsonResponse({
        'liked': liked,
        'likes_count': recipe.likes.count()
    })


@login_required
@require_POST
def recipe_favorite(request, slug):
    """
    Ajouter/retirer des favoris (AJAX)
    """
    recipe = get_object_or_404(Recipe, slug=slug, is_published=True)
    
    if recipe.favorites.filter(id=request.user.id).exists():
        recipe.favorites.remove(request.user)
        favorited = False
    else:
        recipe.favorites.add(request.user)
        favorited = True
    
    return JsonResponse({
        'favorited': favorited
    })


@login_required
def add_comment(request, slug):
    """
    Ajouter un commentaire à une recette
    """
    recipe = get_object_or_404(Recipe, slug=slug, is_published=True)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.recipe = recipe
            comment.author = request.user
            comment.save()
            messages.success(request, 'Votre commentaire a été ajouté avec succès!')
        else:
            messages.error(request, 'Erreur lors de l\'ajout du commentaire.')
    
    return redirect('recipes:detail', slug=slug)


def category_recipes(request, slug):
    """
    Recettes d'une catégorie spécifique
    """
    category = get_object_or_404(Category, slug=slug)
    recipes = Recipe.objects.filter(
        category=category,
        is_published=True
    ).order_by('-created_at')
    
    paginator = Paginator(recipes, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'recipes': page_obj,
        'categories': Category.objects.all()
    }
    return render(request, 'recipes/category.html', context)