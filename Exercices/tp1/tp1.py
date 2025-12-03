import pandas as pd


# 1. Charger tous les fichiers CSV
df1 = pd.read_csv('magasin_A.csv')
df2 = pd.read_csv('magasin_B.csv')
df3 = pd.read_csv('magasin_C.csv')

# 2. Ajouter une colonne `magasin` (A, B ou C)
df1['magasin'] = 'A'
df2['magasin'] = 'B'
df3['magasin'] = 'C'

# 3. Concaténer tous les DataFrames
df_concat = pd.concat([df1, df2, df3], ignore_index=True)
#print(df_concat)

# 4. Nettoyer (doublons, valeurs manquantes)
df = df_concat.drop_duplicates()
df = df.fillna('Non spécifié')
#print(df)

# 5. Calculer `montant_total`
df['montant_total'] = df['quantite'] * df['prix_unitaire']
print(df)

# 6. Créer un rapport Excel avec :
#    - Feuille "Consolidé" : Toutes les données
#    - Feuille "Par magasin" : Totaux par magasin
#    - Feuille "Par vendeur" : Performance des vendeurs
#    - Feuille "Top produits" : 10 produits les plus vendus
ventes_magasin = (df.groupby("magasin")["montant_total"].sum().reset_index()).sort_values('montant_total',ascending=False)
ventes_vendeur = (df.groupby(["vendeur", "magasin"])["montant_total"].sum().reset_index()).sort_values('montant_total',ascending=False)
ventes_vendeur.columns = ["vendeur", "magasin", "montant_total"]
ventes_produit = (df.groupby("produit")["quantite"].sum().reset_index()).sort_values('quantite',ascending=False)

# df['date'] = df['date'].dt.strftime("%Y-%m-%d")


with pd.ExcelWriter('Rapport.xlsx') as writer:
    df.to_excel(writer, sheet_name='Consolidé', index=False)
    ventes_magasin.to_excel(writer, sheet_name='Par magasin', index=False)
    ventes_vendeur.to_excel(writer, sheet_name='Par vendeur', index=False)
    ventes_produit.to_excel(writer, sheet_name='Top produits', index=False)