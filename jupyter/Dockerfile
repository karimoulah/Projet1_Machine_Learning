# Utiliser l'image Jupyter scientifique avec plein de libs déjà incluses
FROM jupyter/scipy-notebook:latest

# Définir le répertoire de travail
WORKDIR /home/jovyan/work

# Installer les dépendances supplémentaires nécessaires à ton projet
RUN pip install --no-cache-dir \
    pymongo \
    scikit-learn \
    pandas \
    matplotlib \
    seaborn \
    xgboost \
    eli5

# Exposer le port Jupyter
EXPOSE 8888
