import requests
import os
from dotenv import load_dotenv
load_dotenv()

#https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}
def weatherCallApi(params):
    # URL de l'API
    urlWeather=os.getenv("API_WEATHER_URL")
    url = urlWeather
    # Votre token d'authentification
    token = os.getenv("API_TOKEN_WEATHER")
    # En-têtes de la requête
    headers = {
        "Accept": "application/json"
    }
    params["appid"]=token
    # Effectuer la requête GET
    response = requests.get(url, params=params, headers=headers)
    # Vérifier si la requête a réussi
    if response.status_code == 200:
        # Traiter la réponse JSON
        data = response.json()
        return data
    else:
        print(f"Erreur {response.status_code}: {response.text}")

