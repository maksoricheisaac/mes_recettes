"""
Formulaires pour la gestion des recettes
"""
from django import forms
from .models import Recipe, Comment, Category


class RecipeForm(forms.ModelForm):
    """
    Formulaire pour créer/modifier une recette
    """
    class Meta:
        model = Recipe
        fields = [
            'title', 'description', 'category', 'ingredients', 'instructions',
            'prep_time', 'cook_time', 'servings', 'difficulty', 'image', 'is_published'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Titre de votre recette'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'rows': 3,
                'placeholder': 'Description courte de votre recette'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
            }),
            'ingredients': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'rows': 8,
                'placeholder': 'Listez les ingrédients, un par ligne\nExemple:\n250g de farine\n3 œufs\n200ml de lait'
            }),
            'instructions': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'rows': 10,
                'placeholder': 'Décrivez les étapes de préparation, une par ligne\nExemple:\nMélanger la farine et les œufs\nAjouter le lait progressivement\nCuire à la poêle'
            }),
            'prep_time': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'min': '0'
            }),
            'cook_time': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'min': '0'
            }),
            'servings': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'min': '1'
            }),
            'difficulty': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajouter une option vide pour la catégorie
        self.fields['category'].empty_label = "Choisir une catégorie"


class CommentForm(forms.ModelForm):
    """
    Formulaire pour ajouter un commentaire
    """
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'rows': 4,
                'placeholder': 'Partagez votre avis sur cette recette...'
            })
        }


class RecipeSearchForm(forms.Form):
    """
    Formulaire de recherche de recettes
    """
    q = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Rechercher une recette...'
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Toutes les catégories",
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
        })
    )
    prep_time = forms.ChoiceField(
        choices=[
            ('', 'Temps de préparation'),
            ('15', 'Moins de 15 minutes'),
            ('30', 'Moins de 30 minutes'),
            ('60', 'Moins d\'1 heure'),
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
        })
    )
    sort = forms.ChoiceField(
        choices=[
            ('-created_at', 'Plus récentes'),
            ('popular', 'Plus populaires'),
            ('created_at', 'Plus anciennes'),
        ],
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
        })
    )