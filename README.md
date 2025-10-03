# MGL7811 – German Credit Report (Docker + NoSQL)

****Auteur : Abdoul Karime DIOP****

****Code Permanent: DIOA14279808
****GitHub : https://github.com/karimoulah********

---

## 🎯 Objectif du projet

Mettre en place un environnement **reproductible** pour exécuter le notebook **`MGL7811_GermanCreditReport.ipynb`** avec les contraintes suivantes :

- Tous les composants (Jupyter/Notebook, etc.) s’exécutent en **conteneurs Docker** ;
- Le dataset n’est **pas lu directement depuis un CSV** par le notebook : il provient d’une **base NoSQL (MongoDB)** ;
- Un évaluateur doit pouvoir **reproduire** et exécuter l’application en quelques commandes.

---

## 🧱 Architecture & flux

```
mgl7811_project/
├─ docker-compose.yml
├─ README.md
├─ .gitignore
├─ data/                       # (à VOUS de déposer german_credit_data.csv ici)
└─ jupyter/
   ├─ Dockerfile               # image Jupyter (Python 3.11 + data stack + pymongo)
   ├─ requirements.txt         # versions figées (pandas, sklearn, matplotlib, ...)
   └─ notebooks/
      ├─ MGL7811_GermanCreditReport.ipynb
```

**Services (docker-compose.yml)**

- `mongo` : **MongoDB 6.0** (stockage NoSQL, persistance via volume `mongo_data`)
- `mongo-express` : UI web d’administration MongoDB (port `8081`)
- `jupyter` : Environnement **Jupyter Lab** (port `8888`) avec dépendances data science + `pymongo`
- `data-loader` : Conteneur éphémère qui **importe** `./data/german_credit_data.csv` → MongoDB (`db=german_credit_data`, `collection=records`)

**Flux de données**

1. Vous déposez `german_credit_data.csv` dans `./data/`
2. `data-loader` exécute `mongoimport` → documents insérés dans MongoDB
3. Le notebook **lit la collection** via `utils_mongo_loader.load_from_mongo()` → `dataset` (pandas DataFrame)
4. Les analyses s’exécutent **sans dépendre du CSV** (source = NoSQL).

**Raisons de l’architecture**

- Respect strict de la contrainte **NoSQL** ;
- Import **idempotent** et reproductible séparé de l’analyse ;
- **mongo-express** facilite la vérification rapide du contenu ;
- **Versions figées** des bibliothèques pour garantir les résultats ;
- Séparation claire des responsabilités (DB / import / notebook).

---

## ⚙️ Prérequis

- **Docker** ≥ 20.x et **Docker Compose** (plugin) ≥ v2.x
- **Git** pour cloner le dépôt
- OS cible : Linux, macOS, ou Windows (**WSL2** recommandé)

> Vérifiez Docker : `docker --version` et `docker compose version`

---

## 🚀 Démarrage rapide (Quickstart)

1) **Cloner** le dépôt et se placer dans le dossier :

```bash
git clone https://github.com/karimoulah/Projet1_Machine_Learning.git
```

2) **Placer le dataset** dans `./data/` :

- Fichier attendu : **`german_credit_data.csv`**
- Format : **ligne d’en-têtes** + séparateur virgule `,`

3) **Lancer l’environnement** :

```bash
docker compose up -d --build
```

4) **Accéder aux interfaces** :

- Jupyter Lab : http://localhost:8888/lab
- Mongo Express : http://localhost:8081/

5) **Ouvrir et exécuter** le notebook :
   `jupyter/notebooks/MGL7811_GermanCreditReport.ipynb`

> La 1ère cellule lit Mongo et crée `dataset` (pandas DataFrame).

---

## 🔧 Configuration & variables d’environnement

- Le service **`jupyter`** reçoit :
  - `MONGO_HOST=mongo`
  - `MONGO_PORT=27017`
- **Volumes** :
  - `./jupyter/notebooks` ↔ `/home/jovyan/work`
  - `./data` ↔ `/home/jovyan/data`
  - `mongo_data` (volume Docker) pour la persistance DB

**Ports par défaut** :

- Jupyter : `8888`
- Mongo Express : `8081`
- MongoDB : `27017`

> Modifiez-les si des conflits existent (voir *Dépannage*).

---

## 📊 Données : format & import

- Le service `data-loader` exécute en interne :
  ```bash
  mongoimport --host mongo \
              --db german_credit_data \
              --collection records \
              --type csv --headerline \
              --file /data/import/german_credit_data.csv \
              --drop
  ```
- **Important** : la **première ligne** du CSV doit contenir les **noms de colonnes**.
- Pour **réimporter** après modification du CSV :
  ```bash
  docker compose run --rm data-loader
  ```

---

## 🧪 Notebook : contenu & bonnes pratiques

Le notebook couvre les points typiques d’une analyse MGL7811 :

- **Partie 1 : Exploration** – taille du dataset, types de variables, distribution de la cible `Risk`
- **Partie 2 : Distributions & relations** – visualisations (countplot, hist, hue=Risk), corrélations pertinentes
- **Partie 3 : Préparation (feature engineering)** – encodage catégoriel, gestion NaN, split train/testxs

**Bonnes pratiques** :

- Conservez les transformations **dans le notebook**, pas dans des scripts externes ;
- Logguez la **version** des libs (pandas, numpy, sklearn) ;
- Commentez les hypothèses et choix (encodage, traitement des NaN, etc.).

---

## 🔒 Sécurité (local)

- Jupyter démarre **sans token** pour simplifier la correction locale. **Ne pas** exposer ce port publiquement.
- Pour activer la protection : remplacez la `CMD` dans `jupyter/Dockerfile` par la commande par défaut de Jupyter et définissez un **token**/**mot de passe**.
- Mongo Express est une UI d’**administration** ; évitez de l’ouvrir sur Internet.

---

## 🧭 Organisation Git (exigence pédagogique)

- Travail quotidien sur **`dev`** ;
- **`main`** ne contient que le **livrable final propre** (pas d’anciens brouillons / fichiers inutiles) ;
- `data/` est **ignoré** (pas de données dans Git).

## ♻️ Reproductibilité & déterminisme

- **Versions figées** dans `jupyter/requirements.txt` ;
- **Import idempotent** via `data-loader` ;
- Notebook autonome : **source = MongoDB** (aucune dépendance lecture CSV pendant l’exécution).

---

## 🧩 Variantes d’architecture (selon ressources)

- **Machine modeste** :

  - Laisser l’architecture telle quelle (3 services + loader).
  - Si nécessaire, **arrêter `mongo-express`** (facultatif) pour économiser de la RAM.
- **Machine puissante** :

  - Ajouter un service **scheduler**/CI (GitHub Actions) pour exécuter des _smoke tests_ (exécuter une cellule de lecture Mongo).
  - Étendre vers d’autres NoSQL (Cassandra, CouchDB) pour comparaison (adapter `data-loader` et `utils_mongo_loader.py`).

---

## ✅ Checklist de validation (pour le correcteur)

- [ ] `docker compose up -d --build` fonctionne sans erreur
- [ ] Le CSV est ignoré par Git (`data/` dans `.gitignore`)
- [ ] `data-loader` importe bien vers Mongo (`db=german_credit_data`, `collection=records`)
- [ ] **Notebook** lit **Mongo** (et non un CSV) et crée `dataset`
- [ ] Analyses/visualisations **s’exécutent** et sont **pertinentes**
- [ ] README présent, clair, avec explication d’architecture et **nom de l’auteur**
- [ ] Branche **`main`** propre, **`dev`** pour l’historique

---

## 🛠️ Dépannage (FAQ technique)

- **Port déjà utilisé** (`8888`, `8081`, `27017`)→ Modifier `docker-compose.yml` (ex. `8889:8888`), relancer `make up`
- **`Permission denied` sur Docker (Linux)**→ Ajouter votre utilisateur au groupe `docker` puis se reconnecter
- **`File not found: german_credit_data.csv`**→ Déposer le fichier dans `./data/`, relancer `make reimport` ou `make up`
- **`Headerline` manquant** (import CSV)→ Vérifier que la **1ère ligne** du CSV contient bien les **en-têtes**
- **Notebook ne voit pas les données**
  → Vérifier `MONGO_HOST=mongo`, `MONGO_PORT=27017` côté service `jupyter`
