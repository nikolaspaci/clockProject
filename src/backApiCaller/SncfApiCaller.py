import requests
import os
from dotenv import load_dotenv
load_dotenv()

def callSncfApi(params,endpoint):
    # URL de l'API
    urlSncf=os.getenv("API_SNCF_URL")
    url = urlSncf+"/"+endpoint
    # Votre token d'authentification
    token = os.getenv("API_TOKEN_SNCF")
    # En-têtes de la requête
    headers = {
        "apiKey": token,
        "Accept": "application/json"
    }
    # Effectuer la requête GET
    response = requests.get(url, params=params, headers=headers)
    # Vérifier si la requête a réussi
    if response.status_code == 200:
        # Traiter la réponse JSON
        data = response.json()
        return data
    else:
        print(f"Erreur {response.status_code}: {response.text}")


def callForJourney(params):
    endpoint = "journeys"
    return callSncfApi(params,endpoint)

def callForStatus(paths,params):
    endpoint = "line_reports/"+paths
    return callSncfApi(params,endpoint) 