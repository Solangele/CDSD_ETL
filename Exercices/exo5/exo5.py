import requests
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

API_KEY = os.getenv('OPENWEATHER_API_KEY')
BASE_URL = 'https://api.openweathermap.org/data/2.5'


# 1. Définir une liste de 10 villes françaises
# 2. Pour chaque ville, récupérer :
#    - Température actuelle
#    - Température ressentie
#    - Humidité
#    - Description
villes = ['Tourcoing', 'Lille', 'Paris', 'Agde', 'Versailles', 'Strasbourg', 'Brest', 'Lyon', 'Bordeaux', 'Mulhouse']

url = f'{BASE_URL}/weather'

meteo_ville = []

for ville in villes : 
    params = {
        'q' : ville,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'fr'
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Lève une erreur si le status code n'est pas 200
        data = response.json()


        meteo_ville.append({
            "ville": ville,
            "temperature": data["main"]["temp"],
            "ressenti": data["main"]["feels_like"],
            "humidite": data["main"]["humidity"],
            "description": data["weather"][0]["description"]
        })
    except requests.exceptions.HTTPError as http_err:
        print(f"⚠️ HTTP error pour {ville} : {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"⚠️ Erreur de requête pour {ville} : {req_err}")
    except KeyError as key_err:
        print(f"⚠️ Données manquantes pour {ville} : {key_err}")

# 3. Créer un DataFrame avec ces informations
df = pd.DataFrame(meteo_ville)
print(df)


# 4. Identifier la ville la plus chaude et la plus froide
plus_chaude = df.nlargest(1,'temperature')[['ville', 'temperature']]
plus_froide = df.nsmallest(1, 'temperature')[['ville', 'temperature']]
print(plus_chaude)
print(plus_froide)


# 5. Calculer la température moyenne
temp_moyenne = df['temperature'].mean()
print(f"La temperature moyenne sur les 10 villes est de {temp_moyenne}")


# 6. Sauvegarder dans `meteo_villes.csv`
df.to_csv('meteo_villes.csv', index=False)


# 7. **Bonus** : Ajouter une gestion d'erreur si une ville n'est pas trouvée
# voir dans la boucle for dans la question 2


# Correction : 
# import requests
# import pandas as pd
# import os
# from dotenv import load_dotenv


# load_dotenv()
# API_KEY = os.getenv('OPENWEATHER_API_KEY')
# BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

# # 1. Définir une liste de 10 villes françaises
# villes = ['Paris', 'Lyon', 'Marseille', 'Toulouse', 'Nice', 
#           'Nantes', 'Strasbourg', 'Montpellier', 'Bordeaux', 'Lille']


# # 2. Pour chaque ville, récupérer :
# #    - Température actuelle
# #    - Température ressentie
# #    - Humidité
# #    - Description
# data_meteo = []

# for ville in villes:
#     try:
#         params = {
#             'q': ville,
#             'appid': API_KEY,
#             'units': 'metric',
#             'lang': 'fr'
#         }

#         response = requests.get(BASE_URL, params=params, timeout=5)
#         response.raise_for_status()
#         data = response.json()
#         data_meteo.append({
#             'ville' : ville,
#             'temperature' : data['main']['temp'],
#             'ressenti' : data['main']['feels_like'],
#             'humidite' : data['main']['humidity'],
#             'description' : data['weather'][0]['description']
#         })
#     except requests.exceptions.RequestException as e:
#         print(f"Erreur lors de la recup des data pour la ville {ville} : {e}")
#         continue


# # 3. Créer un DataFrame avec ces informations
# df = pd.DataFrame(data_meteo)

# # 4. Identifier la ville la plus chaude et la plus froide
# ville_chaude = df.nlargest(1, 'temperature').iloc[0]
# ville_froide = df.nsmallest(1, 'temperature').iloc[0]

# print(f"La ville la plus chaude : {ville_chaude['ville']} {ville_chaude['temperature']}")
# print(f"La ville la plus chaude : {ville_froide['ville']} {ville_froide['temperature']}")


# # 5. Calculer la température moyenne
# temp_moyenne = df['temperature'].mean()
# print(f"Temperature moyenne : {temp_moyenne}")

# # 6. Sauvegarder dans `meteo_villes.csv`
# df.to_csv('meteo_villes.csv', index=False)


# # 7. **Bonus** : Ajouter une gestion d'erreur si une ville n'est pas trouvée