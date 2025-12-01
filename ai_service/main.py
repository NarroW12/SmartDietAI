import os
import base64
import json
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from openai import AzureOpenAI
from dotenv import load_dotenv

# 1. Ładowanie zmiennych środowiskowych
load_dotenv(dotenv_path="../.env")  # Wskazujemy ścieżkę do pliku .env w folderze wyżej

app = FastAPI(title="SmartDiet AI Microservice")

# 2. Konfiguracja klienta Azure OpenAI
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-15-preview",  # Wersja API obsługująca Vision
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)
deployment_name = os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-4o")


# Model odpowiedzi (dla dokumentacji, AI zwraca surowy JSON)
class AIResponse(BaseModel):
    dish_name: str
    calories: int
    protein: float
    carbs: float
    fat: float
    ingredients: list[str]
    advice: str


def encode_image(image_file):
    """Funkcja pomocnicza: zamienia plik obrazu na string Base64"""
    return base64.b64encode(image_file).decode('utf-8')


@app.post("/analyze-food", response_model=AIResponse)
async def analyze_food(
        file: UploadFile = File(...),
        weight_grams: int = Form(None)  # Opcjonalna waga
):
    try:
        # A. Czytanie i kodowanie obrazu
        contents = await file.read()
        base64_image = encode_image(contents)

        # B. Budowanie promptu (instrukcji dla AI)
        system_instruction = "Jesteś ekspertem dietetyki i analizy żywności. Twoim zadaniem jest identyfikacja potrawy ze zdjęcia i wyliczenie wartości odżywczych."

        user_prompt = "Zanalizuj to zdjęcie."
        if weight_grams:
            user_prompt += f" Użytkownik zważył potrawę: waży ona dokładnie {weight_grams} gramów. Wylicz kalorie i makro dla tej konkretnej wagi."
        else:
            user_prompt += " Użytkownik nie podał wagi. Oszacuj wagę standardowej porcji widocznej na talerzu i wylicz dla niej wartości."

        user_prompt += """
        Ważne: Zwróć odpowiedź TYLKO i wyłącznie jako czysty obiekt JSON (bez bloków ```json). 
        Format JSON ma być następujący:
        {
            "dish_name": "Nazwa dania po polsku",
            "calories": 0 (liczba całkowita kcal),
            "protein": 0.0 (białko w gramach),
            "carbs": 0.0 (węglowodany w gramach),
            "fat": 0.0 (tłuszcze w gramach),
            "ingredients": ["lista", "głównych", "składników"],
            "advice": "Krótka, jednozdaniowa porada dietetyczna lub ciekawostka o tym daniu po polsku."
        }
        """

        # C. Wysłanie zapytania do Azure OpenAI
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": [
                    {"type": "text", "text": user_prompt},
                    {"type": "image_url", "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }}
                ]}
            ],
            max_tokens=500,
            temperature=0.3  # Niska temperatura dla bardziej precyzyjnych/faktograficznych danych
        )

        # D. Przetwarzanie odpowiedzi
        raw_content = response.choices[0].message.content

        # Czasami AI dodaje ```json na początku i ``` na końcu, musimy to wyczyścić
        cleaned_content = raw_content.replace("```json", "").replace("```", "").strip()

        data = json.loads(cleaned_content)

        return data

    except Exception as e:
        print(f"Błąd AI Service: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint testowy, żeby sprawdzić czy serwis żyje
@app.get("/")
def health_check():
    return {"status": "AI Service is running", "azure_model": deployment_name}