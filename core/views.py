"""
Vues principales de l'application MesRecettes
"""
from django.views.generic import ListView
from django.db.models import Q, Count
from recipes.models import Recipe, Category


class HomeView(ListView):
    """
    Page d'accueil avec les recettes les plus populaires
    """
    model = Recipe
    template_name = 'core/home.html'
    context_object_name = 'recipes'
    paginate_by = 12

    def get_queryset(self):
        return Recipe.objects.filter(is_published=True).annotate(
            num_likes=Count('likes')
        ).order_by('-num_likes', '-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['featured_recipes'] = Recipe.objects.filter(
            is_published=True, is_featured=True
        ).order_by('-created_at')[:3]
        return context


class SearchView(ListView):
    """
    Page de recherche avec filtres
    """
    model = Recipe
    template_name = 'core/search.html'
    context_object_name = 'recipes'
    paginate_by = 12

    def get_queryset(self):
        queryset = Recipe.objects.filter(is_published=True)
        
        # Recherche par mot-clé
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(ingredients__icontains=query)
            )

        # Filtrage par catégorie
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category_id=category)

        # Filtrage par temps de préparation
        prep_time = self.request.GET.get('prep_time')
        if prep_time:
            if prep_time == '15':
                queryset = queryset.filter(prep_time__lte=15)
            elif prep_time == '30':
                queryset = queryset.filter(prep_time__lte=30)
            elif prep_time == '60':
                queryset = queryset.filter(prep_time__lte=60)

        # Tri
        sort_by = self.request.GET.get('sort', '-created_at')
        if sort_by == 'popular':
            queryset = queryset.annotate(
                num_likes=Count('likes')
            ).order_by('-num_likes')
        elif sort_by == 'newest':
            queryset = queryset.order_by('-created_at')
        elif sort_by == 'oldest':
            queryset = queryset.order_by('created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['query'] = self.request.GET.get('q', '')
        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_prep_time'] = self.request.GET.get('prep_time', '')
        context['selected_sort'] = self.request.GET.get('sort', '-created_at')
        return context