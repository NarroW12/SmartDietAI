# web_backend/diet_app/views.py
import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import MealLog

# Adres Twojego mikroserwisu FastAPI (AI)
AI_SERVICE_URL = "http://127.0.0.1:8001/analyze-food"


@login_required
def dashboard_view(request):
    """Główny widok: formularz uploadu + lista posiłków z dzisiaj"""

    if request.method == 'POST' and request.FILES.get('meal_photo'):
        photo = request.FILES['meal_photo']
        weight = request.POST.get('weight')

        try:
            # 1. Komunikacja z mikroserwisem AI (FastAPI)
            files = {'file': (photo.name, photo.file, photo.content_type)}
            data = {}
            if weight:
                data['weight_grams'] = int(weight)

            # Wysyłamy żądanie do portu 8001
            response = requests.post(AI_SERVICE_URL, files=files, data=data)
            response.raise_for_status()  # Rzuć błąd jeśli status != 200

            ai_result = response.json()  # Otrzymujemy czysty JSON z AI

            # 2. Zapis w bazie Django
            MealLog.objects.create(
                user=request.user,
                image=photo,
                user_estimated_weight=weight if weight else None,
                nutrition_data=ai_result,
                calories=ai_result.get('calories', 0)
            )

            return redirect('dashboard')

        except requests.RequestException as e:
            error_message = f"Błąd połączenia z serwisem AI: {e}"
            return render(request, 'dashboard.html', {'error': error_message})

    # Pobierz dzisiejsze posiłki użytkownika
    from django.utils import timezone
    today_meals = MealLog.objects.filter(
        user=request.user,
        created_at__date=timezone.now().date()
    ).order_by('-created_at')

    # Suma kalorii z dzisiaj
    total_calories_today = sum(meal.calories for meal in today_meals)

    context = {
        'meals': today_meals,
        'total_calories': total_calories_today
    }
    return render(request, 'dashboard.html', context)


@login_required
def calendar_api(request):
    """API zwracające dane dla kalendarza JS"""
    meals = MealLog.objects.filter(user=request.user)
    events = []

    # Grupowanie posiłków, aby nie zaśmiecać kalendarza
    # (Można to zrobić lepiej agregacją SQL, ale pętla jest czytelniejsza na start)
    for meal in meals:
        dish_name = meal.nutrition_data.get('dish_name', 'Posiłek')
        events.append({
            'title': f"{dish_name} ({meal.calories} kcal)",
            'start': meal.created_at.isoformat(),
            'backgroundColor': '#10B981' if meal.calories < 500 else '#EF4444',  # Tailwind green/red colors
            'borderColor': 'transparent'
        })

    return JsonResponse(events, safe=False)