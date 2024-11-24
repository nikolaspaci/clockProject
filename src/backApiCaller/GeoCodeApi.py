import requests
import os
from dotenv import load_dotenv
load_dotenv()

def geoCodeCallApi(params):
    # URL de l'API
    urlWeather=os.getenv("API_WEATHER_GEOCODE_URL")
    # Votre token d'authentification
    token = os.getenv("API_TOKEN_WEATHER")
    # En-têtes de la requête
    headers = {
        "Accept": "application/json"
    }
    #add in map the token
    params["appid"]=token
    # Effectuer la requête GET
    response = requests.get(urlWeather, params=params, headers=headers)
    # Vérifier si la requête a réussi
    if response.status_code == 200:
        # Traiter la réponse JSON
        data = response.json()
        return data
    else:
        print(f"Erreur {response.status_code}: {response.text}")


def getLatitudeAndLongitude(address):
    urlNomi=os.getenv("API_URL_NOMINATIM")
    url = f"{urlNomi}?q={address}&format=json&limit=1"
    params = {
        "q": address,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "apitc001/1.0"
    }
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data:
            return {"lat": float(data[0]["lat"]), "lon": float(data[0]["lon"])}
    return None
