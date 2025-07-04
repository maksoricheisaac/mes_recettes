"""
Vues pour la gestion des comptes utilisateurs
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import UserRegistrationForm, ProfileUpdateForm, UserUpdateForm
from .models import Profile
from recipes.models import Recipe


def register(request):
    """
    Vue d'inscription
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Votre compte a été créé avec succès!')
            return redirect('core:home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile_edit(request):
    """
    Vue de modification du profil
    """
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, 
            request.FILES, 
            instance=request.user.profile
        )
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès!')
            return redirect('accounts:profile', username=request.user.username)
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'accounts/profile_edit.html', context)


def profile_view(request, username):
    """
    Vue du profil utilisateur
    """
    user = get_object_or_404(User, username=username)
    profile = user.profile
    
    # Récupérer les recettes de l'utilisateur
    user_recipes = Recipe.objects.filter(
        author=user, 
        is_published=True
    ).order_by('-created_at')
    
    # Pagination des recettes
    paginator = Paginator(user_recipes, 9)
    page_number = request.GET.get('page')
    recipes = paginator.get_page(page_number)
    
    # Récupérer les favoris si c'est le propre profil de l'utilisateur
    favorites = None
    if request.user.is_authenticated and request.user == user:
        favorites = Recipe.objects.filter(
            favorites=user,
            is_published=True
        ).order_by('-created_at')[:6]
    
    context = {
        'profile_user': user,
        'profile': profile,
        'recipes': recipes,
        'favorites': favorites,
        'is_own_profile': request.user == user if request.user.is_authenticated else False
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def favorites_view(request):
    """
    Vue des recettes favorites de l'utilisateur
    """
    favorite_recipes = Recipe.objects.filter(
        favorites=request.user,
        is_published=True
    ).order_by('-created_at')
    
    paginator = Paginator(favorite_recipes, 12)
    page_number = request.GET.get('page')
    recipes = paginator.get_page(page_number)
    
    context = {
        'recipes': recipes,
        'title': 'Mes recettes favorites'
    }
    return render(request, 'accounts/favorites.html', context)