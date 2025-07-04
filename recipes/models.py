"""
Modèles pour la gestion des recettes
"""
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from PIL import Image


class Category(models.Model):
    """
    Catégorie de recette
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Nom")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    description = models.TextField(blank=True, verbose_name="Description")
    color = models.CharField(max_length=7, default='#3B82F6', verbose_name="Couleur")
    
    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('recipes:category', kwargs={'slug': self.slug})


class Recipe(models.Model):
    """
    Modèle principal pour les recettes
    """
    DIFFICULTY_CHOICES = [
        ('facile', 'Facile'),
        ('moyen', 'Moyen'),
        ('difficile', 'Difficile'),
    ]

    title = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    description = models.TextField(verbose_name="Description")
    ingredients = models.TextField(verbose_name="Ingrédients")
    instructions = models.TextField(verbose_name="Instructions")
    
    # Métadonnées
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes', verbose_name="Auteur")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Catégorie")
    
    # Temps et difficulté
    prep_time = models.PositiveIntegerField(verbose_name="Temps de préparation (minutes)")
    cook_time = models.PositiveIntegerField(verbose_name="Temps de cuisson (minutes)")
    servings = models.PositiveIntegerField(verbose_name="Nombre de portions")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, verbose_name="Difficulté")
    
    # Image
    image = models.ImageField(upload_to='recipes/', blank=True, null=True, verbose_name="Image")
    
    # Statut
    is_published = models.BooleanField(default=True, verbose_name="Publié")
    is_featured = models.BooleanField(default=False, verbose_name="Mis en avant")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")
    
    # Relations many-to-many
    likes = models.ManyToManyField(User, related_name='liked_recipes', blank=True, verbose_name="J'aime")
    favorites = models.ManyToManyField(User, related_name='favorite_recipes', blank=True, verbose_name="Favoris")

    class Meta:
        verbose_name = "Recette"
        verbose_name_plural = "Recettes"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
        # Redimensionner l'image si nécessaire
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 800 or img.width > 800:
                output_size = (800, 800)
                img.thumbnail(output_size)
                img.save(self.image.path)

    def get_absolute_url(self):
        return reverse('recipes:detail', kwargs={'slug': self.slug})

    @property
    def total_time(self):
        return self.prep_time + self.cook_time

    @property
    def likes_count(self):
        return self.likes.count()

    @property
    def comments_count(self):
        return self.comments.count()

    def get_ingredients_list(self):
        """Retourne la liste des ingrédients"""
        return [ingredient.strip() for ingredient in self.ingredients.split('\n') if ingredient.strip()]

    def get_instructions_list(self):
        """Retourne la liste des instructions"""
        return [instruction.strip() for instruction in self.instructions.split('\n') if instruction.strip()]


class Comment(models.Model):
    """
    Commentaire sur une recette
    """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments', verbose_name="Recette")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Auteur")
    content = models.TextField(verbose_name="Contenu")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")
    is_approved = models.BooleanField(default=True, verbose_name="Approuvé")

    class Meta:
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"
        ordering = ['-created_at']

    def __str__(self):
        return f"Commentaire de {self.author.username} sur {self.recipe.title}"