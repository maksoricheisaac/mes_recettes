"""
Modèles pour la gestion des utilisateurs étendus
"""
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image


class Profile(models.Model):
    """
    Profil utilisateur étendu avec informations supplémentaires
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, verbose_name="Biographie")
    avatar = models.ImageField(
        upload_to='profiles/avatars/', 
        blank=True, 
        null=True,
        verbose_name="Photo de profil"
    )
    location = models.CharField(max_length=100, blank=True, verbose_name="Localisation")
    website = models.URLField(blank=True, verbose_name="Site web")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profils"

    def __str__(self):
        return f"Profil de {self.user.username}"

    def get_absolute_url(self):
        return reverse('accounts:profile', kwargs={'username': self.user.username})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Redimensionner l'avatar si nécessaire
        if self.avatar:
            img = Image.open(self.avatar.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.avatar.path)

    @property
    def recipes_count(self):
        return self.user.recipes.filter(is_published=True).count()

    @property
    def likes_received(self):
        return sum(recipe.likes.count() for recipe in self.user.recipes.all())


# Signal pour créer automatiquement un profil lors de la création d'un utilisateur
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()