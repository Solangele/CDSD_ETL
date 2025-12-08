import os
import pandas as pd

from Exercices.tp2.src.pipeline.pipeline import ETLPipeline        # ETLPipeline générique déjà existante
from src.extractors.extractors import APIExtractor, CSVExtractor

class ApiPipeline(ETLPipeline):
    """
    Pipeline ETL concret basé sur une API publique (JSONPlaceholder).

    Étapes :
    1) EXTRACT  : appel HTTP GET sur /posts
    2) TRANSFORM:
         - nettoyage (doublons, espaces, colonnes vides)
         - validation des colonnes essentielles
         - enrichissement (longueur du titre)
    3) LOAD     : écriture en Excel dans data/output/posts_api.xlsx
    """

    def _extract(self) -> pd.DataFrame:
        """Extraction des posts depuis l'API JSONPlaceholder."""

        # 1) Récupérer l'URL de base de l'API depuis la config
        base_url = self.config["api"]["base_url"]

        # 2) Créer un extracteur API (pas de clé API nécessaire ici)
        self.extractor = APIExtractor(
            logger=self.logger,
            base_url=base_url,
            api_key=os.getenv("OPENWEATHER_API_KEY")
        )

        self.extractor = CSVExtractor

        # 3) Appel de l'endpoint /posts avec une limite de 30 éléments
        params = {"_limit": 30}

        df = self.extractor.extract("products", params=params)

        # À ce stade, df est un DataFrame avec les colonnes JSONPlaceholder :
        # userId, id, title, body
        return df
    
    def _transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """Nettoie, valide et enrichit les données issues de l'API."""

        # 1) Nettoyage générique (doublons, colonnes vides, trim des strings)
        df_clean = self.transformer.clean(data)

        # 2) Validation de la présence de colonnes clés
        required_cols = ["produit_id", "nom", "categorie", "fournisseur"]
        self.transformer.validate(df_clean, required_cols)

    
    def _load(self, data: pd.DataFrame) -> None:
        """Charge les données transformées dans un fichier Excel."""

        # Dossier de sortie depuis la config
        output_dir = self.config["paths"]["output"]
        os.makedirs(output_dir, exist_ok=True)

        # Nom du fichier de sortie Excel
        output_file = os.path.join(output_dir, "rapport_ventes.xlsx")

        # Utilisation du DataLoader pour écrire en Excel
        self.loader.load_excel(
            df=data,
            filepath=output_file,
            sheet_name="PostsAPI"
        )

        # À la fin, on aura un fichier data/output/posts_api.xlsx