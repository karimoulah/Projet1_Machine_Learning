FROM python:3.11-slim

# Installation des dépendances système utiles
RUN apt-get update && apt-get install -y build-essential git curl && rm -rf /var/lib/apt/lists/*

# Créer un utilisateur non-root pour Jupyter (bonne pratique)
ENV USER=jovyan
ENV HOME=/home/$USER
RUN useradd -m -s /bin/bash $USER

WORKDIR $HOME

# Copier requirements (notebook libs)
COPY requirements.txt $HOME/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copier notebooks
COPY notebooks/ $HOME/work/

RUN chown -R $USER:$USER $HOME
USER $USER

# Lancer JupyterLab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--NotebookApp.token=''", "--NotebookApp.allow_origin='*'"]
