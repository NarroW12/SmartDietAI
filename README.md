# 🍏 SmartDiet AI

**SmartDiet AI** to nowoczesna aplikacja webowa, która pomaga śledzić dietę za pomocą zdjęć. System wykorzystuje architekturę mikroserwisów, łącząc **Django** (zarządzanie danymi i interfejs) oraz **FastAPI** zintegrowane z **Azure OpenAI (GPT-4o)** do analizy wizualnej posiłków.

---

## ✨ Główne Funkcjonalności

* 📸 **Analiza AI:** Rozpoznawanie potraw ze zdjęcia i automatyczne szacowanie składników.
* ⚖️ **Precyzja:** Możliwość podania wagi potrawy dla dokładniejszego wyliczenia makroskładników.
* 📅 **Kalendarz Kalorii:** Interaktywny widok tygodniowy/miesięczny (FullCalendar) wizualizujący spożycie.
* 💾 **Hybrid Storage:** Zapisywanie pełnych danych z AI jako JSON w bazie PostgreSQL (`JSONField`).
* 📱 **Mobile First:** Responsywny interfejs użytkownika oparty na Tailwind CSS.

---

## 🛠️ Technologia

**Backend & AI:**
* **Django 5.x:** Główny system, ORM, Auth, Templating.
* **FastAPI:** Mikroserwis przetwarzający obrazy i komunikujący się z Azure.
* **PostgreSQL:** Baza danych (wykorzystanie `JSONField`).
* **Azure OpenAI (GPT-4o Vision):** Model AI analizujący zdjęcia.

**Frontend:**
* **HTML5 / Django Templates**
* **Tailwind CSS** (CDN)
* **FullCalendar.js**

---

## 📂 Struktura Projektu

```text
smart_diet_project/
├── .env                  # Konfiguracja i klucze API (nieudostępniane w repo)
├── ai_service/           # MIKROSERWIS 1: Logika AI (FastAPI)
│   ├── main.py           # Endpointy FastAPI
│   └── requirements.txt  # Zależności dla serwisu AI
└── web_backend/          # MIKROSERWIS 2: Aplikacja Webowa (Django)
    ├── diet_app/         # Logika biznesowa (Views, Models)
    ├── config/           # Ustawienia projektu Django
    ├── media/            # Przechowywanie zdjęć posiłków
    └── manage.py

🚀 Instalacja i Konfiguracja

1. Przygotowanie środowiska

W głównym folderze projektu wykonaj:
Bash

# Utwórz wirtualne środowisko
python -m venv venv

# Aktywuj je
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Zainstaluj wymagane biblioteki
pip install django djangorestframework psycopg2-binary requests fastapi uvicorn openai python-dotenv Pillow

2. Konfiguracja zmiennych (.env)

Utwórz plik .env w głównym katalogu smart_diet_project/ i uzupełnij kluczami Azure:
Ini, TOML

AZURE_OPENAI_API_KEY=twoj_klucz_z_azure_portal
AZURE_OPENAI_ENDPOINT=[https://twoja-nazwa.openai.azure.com/](https://twoja-nazwa.openai.azure.com/)
AZURE_DEPLOYMENT_NAME=gpt-4o

3. Baza Danych (PostgreSQL)

    Upewnij się, że masz zainstalowany PostgreSQL.

    Utwórz pustą bazę danych o nazwie diet_db.

    Sprawdź ustawienia w web_backend/config/settings.py (sekcja DATABASES) i dostosuj użytkownika/hasło.

    Wykonaj migracje:

Bash

cd web_backend
python manage.py makemigrations
python manage.py migrate

    Utwórz konto administratora (niezbędne do logowania):

Bash

python manage.py createsuperuser

▶️ Uruchamianie Systemu

System wymaga uruchomienia dwóch oddzielnych terminali.

Terminal 1: Mikroserwis AI (Port 8001)

Bash

# Będąc w folderze smart_diet_project/
cd ai_service
uvicorn main:app --reload --port 8001

Terminal 2: Aplikacja Django (Port 8000)

Bash

# Będąc w folderze smart_diet_project/
cd web_backend
python manage.py runserver

📱 Jak korzystać?

    Otwórz przeglądarkę pod adresem: http://127.0.0.1:8000/

    Zaloguj się danymi superusera.

    Kliknij przycisk aparatu, wgraj zdjęcie jedzenia (opcjonalnie podaj wagę).

    Ciesz się automatyczną analizą i wykresem w kalendarzu!
