# web_backend/diet_app/models.py
from django.db import models
from django.contrib.auth.models import User


class MealLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='meals/')  # Zdjęcie dania
    created_at = models.DateTimeField(auto_now_add=True)  # Data dodania

    # Opcjonalna waga podana przez użytkownika (dla większej precyzji)
    user_estimated_weight = models.IntegerField(null=True, blank=True)

    # KLUCZOWE: Tu zapisujemy całą odpowiedź z FastAPI (Azure AI)
    # Dzięki temu mamy: dish_name, ingredients, advice, makroskładniki w jednym miejscu
    nutrition_data = models.JSONField(default=dict, blank=True)

    # Pola wyciągnięte "na wierzch" dla łatwiejszego sumowania w kalendarzu
    calories = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # Automatycznie wyciągamy kalorie z JSONa, jeśli istnieją, dla szybszego dostępu
        if self.nutrition_data and 'calories' in self.nutrition_data:
            self.calories = int(self.nutrition_data['calories'])
        super().save(*args, **kwargs)

    def __str__(self):
        dish_name = self.nutrition_data.get('dish_name', 'Nieznane danie')
        return f"{self.user.username} - {dish_name} ({self.created_at.date()})"