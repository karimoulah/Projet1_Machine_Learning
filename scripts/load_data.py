import pandas as pd
from pymongo import MongoClient
import os

# Chemin du fichier CSV (monté dans le conteneur)
csv_path = "/data/import/german_credit_data.csv"

if not os.path.exists(csv_path):
    raise FileNotFoundError(f"⚠️ Le fichier {csv_path} est introuvable. Vérifiez le montage du volume.")

# Lecture du CSV
df = pd.read_csv(csv_path)
print(f"✅ Dataset chargé depuis {csv_path}, {df.shape[0]} lignes et {df.shape[1]} colonnes.")

# Connexion à MongoDB (nom du service docker = 'mongo')
client = MongoClient("mongodb://mongo:27017/")
db = client["german_credit_data"]
collection = db["records"]

# Nettoyer la collection avant d’insérer
collection.delete_many({})
print("🗑️ Anciennes données supprimées.")

# Insertion des données
collection.insert_many(df.to_dict("records"))
print(f"✅ {df.shape[0]} enregistrements insérés dans MongoDB.")
