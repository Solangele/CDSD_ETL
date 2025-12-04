import requests
import pandas as pd


# 1. Récupérer tous les pays d'Europe
response = requests.get('https://restcountries.com/v3.1/region/europe')
pays_europe = response.json()

# 2. Créer un DataFrame avec : nom, capitale, population, superficie
response = requests.get('https://restcountries.com/v3.1/region/europe?fields=name,capital,population,area')
data = response.json()

final_data = []

for country in data:
    capital = country.get("capital")
    if isinstance(capital, list) and len(capital) > 0:
        capital = capital[0]
    else:
        capital = "N/A"
    final_data.append({
        "nom": country["name"]["common"],
        "capitale": capital,   
        "population": country.get("population", 0),
        "superficie": country.get("area", 0)
    })

df = pd.DataFrame(final_data)


# 3. Calculer la densité de population (population / superficie)
df["density"] = (df["population"] / df["superficie"].replace(0, pd.NA)).round(2)
df = df.sort_values(by="density", ascending=False)
#print(df)

# 4. Identifier les 5 pays les plus peuplés d'Europe
pays_peuples5 = df.sort_values(by="population", ascending=False).head(5)
#print(pays_peuples5)


# 5. Calculer la population totale de l'Europe
total_pop = df["population"].sum()

#print(f"Population totale en europe : {total_pop}")


# 6. Trouver le pays avec la plus grande densité
max_density = df.sort_values(by="density", ascending=False)
print(max_density)
max_density_value = df["density"].max()

# 7. Sauvegarder les résultats dans `pays_europe.xlsx`
with pd.ExcelWriter('pays_europe.xlsx', engine = 'openpyxl') as writer :
    df.to_excel(writer, sheet_name='pays', index=False)
    pays_peuples5.to_excel(writer, sheet_name='5pays_plus_peuples', index=False)
    pd.DataFrame({"population_totale": [total_pop]}).to_excel(
        writer, sheet_name='population_totale', index=False
    )
    max_density.to_excel(writer, sheet_name='densite', index=False)
    

# Correction
# import requests
# import pandas as pd

# # 1. Récupérer tous les pays d'Europe
# response = requests.get("https://restcountries.com/v3.1/region/europe")
# pays_europe = response.json()

# # 2. Créer un DataFrame avec : nom, capitale, population, superficie
# data = []
# for pays in pays_europe:
#     data.append({
#         'nom' : pays.get('name').get('common'),
#         'capitale' : pays.get('capital')[0],
#         'population' : pays.get('population',0),
#         'superficie' : pays.get('area')
#     })

# df = pd.DataFrame(data)
# print(df)

# # 3. Calculer la densité de population (population / superficie)
# df['densite'] = df['population'] / df['superficie']

# # 4. Identifier les 5 pays les plus peuplés d'Europe
# top5_population = df.nlargest(5, 'population')[['nom','population']]
# print("top 5 population :")
# print(top5_population)

# # 5. Calculer la population totale de l'Europe
# population_total =df['population'].sum()
# print(f"population total en europe : {population_total}")

# # 6. Trouver le pays avec la plus grande densité
# pays_dense = df.nlargest(1, 'densite')[['nom','densite']]
# print("pay le plus dense :")
# print(f"{pays_dense.iloc[0]['nom']} avec {pays_dense.iloc[0]['densite']}")

# # 7. Sauvegarder les résultats dans `pays_europe.xlsx`
# df.to_excel('pays_europe.xlsx', index=False)