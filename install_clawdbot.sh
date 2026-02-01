#!/bin/bash

# Script d'installation pour ClawdBot (OpenClaw / Moltbot)
# Note: Ce script est un modèle (template). Vous devez mettre à jour la variable REPO_URL
# avec l'adresse réelle du dépôt GitHub du projet une fois qu'elle est connue.

# Configuration
REPO_URL="https://github.com/EXEMPLE/clawdbot-repo.git" # <--- METTRE A JOUR ICI
INSTALL_DIR="clawdbot_install"

echo "=================================================="
echo "   Installation de ClawdBot (Mode Sandbox)"
echo "=================================================="

# 1. Vérification des pré-requis
echo "[1/4] Vérification des outils nécessaires..."

if ! command -v git &> /dev/null; then
    echo "ERREUR: git n'est pas installé."
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "ERREUR: python3 n'est pas installé."
    exit 1
fi

echo "Outils détectés : Git et Python3."

# 2. Clonage du dépôt
echo "[2/4] Préparation du répertoire du projet..."

if [ -d "$INSTALL_DIR" ]; then
    echo "Le répertoire '$INSTALL_DIR' existe déjà."
else
    # NOTE: Dans un cas réel, on décommenterait la ligne suivante :
    # git clone "$REPO_URL" "$INSTALL_DIR"

    # Pour la démonstration, on crée le dossier manuellement
    echo "Simulation du clonage de $REPO_URL..."
    mkdir -p "$INSTALL_DIR"

    # Création de fichiers factices pour simuler le contenu du dépôt
    echo "requests" > "$INSTALL_DIR/requirements.txt"
    echo "openai" >> "$INSTALL_DIR/requirements.txt"
    echo "anthropic" >> "$INSTALL_DIR/requirements.txt"
    echo "python-dotenv" >> "$INSTALL_DIR/requirements.txt"

    echo "print('ClawdBot démarré avec succès !')" > "$INSTALL_DIR/main.py"

    echo "Dossier créé et fichiers simulés."
fi

# 3. Configuration de l'environnement virtuel
echo "[3/4] Configuration de l'environnement virtuel Python..."

cd "$INSTALL_DIR" || exit

if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Environnement virtuel 'venv' créé."
else
    echo "L'environnement virtuel existe déjà."
fi

# 4. Installation des dépendances
echo "[4/4] Installation des dépendances..."

# Activation de l'environnement virtuel
source venv/bin/activate

# Mise à jour de pip
pip install --upgrade pip > /dev/null 2>&1

# Installation depuis requirements.txt
if [ -f "requirements.txt" ]; then
    echo "Installation des paquets listés dans requirements.txt..."
    pip install -r requirements.txt
else
    echo "Aucun fichier requirements.txt trouvé."
fi

echo ""
echo "=================================================="
echo "   Installation terminée !"
echo "=================================================="
echo "Pour lancer le bot :"
echo "1. cd $INSTALL_DIR"
echo "2. source venv/bin/activate"
echo "3. python main.py"
echo ""
echo "N'oubliez pas de configurer vos clés API (souvent dans un fichier .env)."
