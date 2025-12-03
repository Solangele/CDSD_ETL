import pandas as pd

# 1. Charger les données avec Pandas
df = pd.read_excel('ventes_janvier.xlsx')
#print(df)

# 2. Nettoyer :
#    - Supprimer les doublons
#    - Remplir les valeurs manquantes de `region` par "Non spécifié"
#    - Convertir `date` en datetime
df = df.drop_duplicates()
df = df.fillna('Non spécifié')
df['date'] = pd.to_datetime(df['date'])

#print(df)


# 3. Transformer :
#    - Créer `montant_total` = quantite × prix_unitaire
#    - Extraire le `jour` et `jour_semaine` de la date
df['montant_total'] = df['quantite'] * df['prix_unitaire']
df['jour'] = df['date'].dt.day
df['jour_semaine'] = df['date'].dt.day_name()
#print(df)


# 4. Analyser :
#    - Total des ventes par région
#    - Produit le plus vendu (en quantité)
#    - Jour de la semaine avec le plus de ventes
ventes_region = (df.groupby("region")["montant_total"].sum().reset_index())
produits_vendus = (df.groupby("produit")["quantite"].sum().sort_values(ascending=False).head(1).reset_index())
jour_vendeur = df.groupby('jour_semaine')["montant_total"].sum().sort_values(ascending=False).head(1)
print(jour_vendeur)


# 5. Créer un fichier Excel avec 3 feuilles :
#    - Feuille "Données" : Données nettoyées
#    - Feuille "Par région" : Agrégation par région
#    - Feuille "Par produit" : Agrégation par produit
df['date'] = df['date'].dt.strftime("%Y-%m-%d")
with pd.ExcelWriter('Resultats_donnees.xlsx') as writer:
    df.to_excel(writer, sheet_name='Données', index=False)
    ventes_region.to_excel(writer, sheet_name='Par région', index=False)
    produits_vendus.to_excel(writer, sheet_name='Par produit', index=False)