#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'installation et de configuration pour le Contract Tagger
================================================================

Ce script installe automatiquement les dépendances et configure
l'environnement pour le tagging automatique de contrats.

Usage: python setup_contract_tagger.py
"""

import subprocess
import sys
import os
import urllib.request
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_command(command, description):
    """Exécute une commande système avec gestion d'erreur"""
    logger.info(f"Exécution: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        logger.info(f"✓ {description} - Succès")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"✗ {description} - Erreur: {e.stderr}")
        return False

def install_requirements():
    """Installe les requirements Python"""
    logger.info("Installation des dépendances Python...")
    
    # Vérifier si le fichier requirements existe
    if not os.path.exists("contract_tagger_requirements.txt"):
        logger.error("Fichier contract_tagger_requirements.txt introuvable!")
        return False
    
    # Installation des packages
    success = run_command(
        f"{sys.executable} -m pip install -r contract_tagger_requirements.txt",
        "Installation des packages Python"
    )
    
    return success

def download_spacy_models():
    """Télécharge et installe les modèles spaCy"""
    logger.info("Installation des modèles spaCy...")
    
    models = [
        ("fr_core_news_sm", "Modèle français"),
        ("en_core_web_sm", "Modèle anglais (fallback)")
    ]
    
    success_count = 0
    for model_name, description in models:
        success = run_command(
            f"{sys.executable} -m spacy download {model_name}",
            f"Installation du {description}"
        )
        if success:
            success_count += 1
    
    return success_count > 0  # Au moins un modèle installé

def download_nltk_data():
    """Télécharge les données NLTK nécessaires"""
    logger.info("Téléchargement des données NLTK...")
    
    try:
        import nltk
        
        # Données essentielles pour le traitement de texte
        datasets = ['punkt', 'stopwords', 'wordnet', 'averaged_perceptron_tagger']
        
        for dataset in datasets:
            try:
                nltk.download(dataset, quiet=True)
                logger.info(f"✓ Dataset NLTK '{dataset}' téléchargé")
            except Exception as e:
                logger.warning(f"⚠ Échec téléchargement '{dataset}': {e}")
        
        return True
    except ImportError:
        logger.error("NLTK n'est pas installé!")
        return False

def create_sample_contract():
    """Crée un fichier d'exemple de contrat pour les tests"""
    sample_contract = """CONTRAT DE VENTE

Article 1 - Parties
Entre la société ABC TECHNOLOGIES SARL, au capital de 50 000 euros, immatriculée au RCS de Paris sous le numéro 123 456 789, ayant son siège social au 123 Avenue des Champs-Élysées, 75008 Paris, représentée par son gérant Monsieur Jean DUPONT, ci-après dénommée "le Vendeur",

Et la société XYZ SOLUTIONS SA, au capital de 200 000 euros, immatriculée au RCS de Lyon sous le numéro 987 654 321, ayant son siège social au 456 Rue de la République, 69002 Lyon, représentée par sa directrice générale Madame Marie MARTIN, ci-après dénommée "l'Acheteur",

Il a été convenu et arrêté ce qui suit :

Article 2 - Objet du contrat
Le présent contrat a pour objet la vente par le Vendeur à l'Acheteur de matériel informatique comprenant :
- 50 ordinateurs portables de marque Dell
- 20 écrans 24 pouces
- 10 imprimantes laser
- Accessoires divers (souris, claviers, câbles)

L'ensemble selon les spécifications techniques détaillées en annexe 1 du présent contrat.

Article 3 - Prix et modalités de paiement
Le prix total de la vente s'élève à la somme de CENT MILLE EUROS (100 000 €) HT, soit 120 000 euros TTC.

Le paiement sera effectué selon les modalités suivantes :
- Un acompte de 30% à la signature du présent contrat
- Le solde à la livraison, sur présentation de la facture

Toute somme non payée à l'échéance portera de plein droit intérêt au taux légal majoré de 3 points.

Article 4 - Livraison
La livraison aura lieu dans un délai maximum de 30 jours ouvrés à compter de la réception de l'acompte, aux locaux de l'Acheteur.

Les risques sont transférés à l'Acheteur lors de la remise du matériel au transporteur.

Article 5 - Garanties
Le Vendeur garantit la conformité du matériel livré aux spécifications convenues. Il garantit également le matériel contre tout vice de fabrication pendant une période de 24 mois à compter de la livraison.

En cas de défaillance du matériel pendant la période de garantie, le Vendeur s'engage à procéder à la réparation ou au remplacement du matériel défaillant dans un délai de 72 heures.

Article 6 - Responsabilité
La responsabilité du Vendeur est limitée au remplacement ou à la réparation du matériel défaillant. En aucun cas, le Vendeur ne pourra être tenu responsable des dommages indirects ou consécutifs.

Article 7 - Force majeure
Les parties ne peuvent être tenues pour responsables si la non-exécution ou le retard dans l'exécution de l'une quelconque de leurs obligations décrites dans le présent contrat découle d'un cas de force majeure.

Article 8 - Résiliation
En cas de manquement grave de l'une des parties aux obligations du présent contrat, celui-ci pourra être résilié de plein droit par l'autre partie, après mise en demeure restée sans effet pendant quinze jours.

Article 9 - Confidentialité
Chaque partie s'engage à maintenir strictement confidentielles toutes les informations techniques, commerciales ou financières de l'autre partie dont elle aura eu connaissance dans le cadre de l'exécution du présent contrat.

Article 10 - Juridiction compétente
Tout litige relatif à l'interprétation ou à l'exécution du présent contrat sera de la compétence exclusive du Tribunal de Commerce de Paris.

Le présent contrat est soumis au droit français.

Article 11 - Signature
Le présent contrat est établi en deux exemplaires originaux.

Fait à Paris, le [DATE]

Le Vendeur                           L'Acheteur
Jean DUPONT                          Marie MARTIN
Gérant ABC TECHNOLOGIES SARL         Directrice XYZ SOLUTIONS SA"""

    with open("sample_contract.txt", "w", encoding="utf-8") as f:
        f.write(sample_contract)
    
    logger.info("✓ Fichier d'exemple 'sample_contract.txt' créé")
    return True

def test_installation():
    """Teste que l'installation fonctionne correctement"""
    logger.info("Test de l'installation...")
    
    try:
        # Import des modules principaux
        import pandas as pd
        import nltk
        import sklearn
        logger.info("✓ Modules Python importés avec succès")
        
        # Test spaCy
        try:
            import spacy
            try:
                nlp = spacy.load("fr_core_news_sm")
                logger.info("✓ Modèle spaCy français chargé avec succès")
            except OSError:
                try:
                    nlp = spacy.load("en_core_web_sm")
                    logger.info("✓ Modèle spaCy anglais chargé avec succès (fallback)")
                except OSError:
                    logger.warning("⚠ Aucun modèle spaCy disponible")
        except ImportError:
            logger.error("✗ spaCy non disponible")
            return False
        
        # Test du script principal
        try:
            from contract_tagger import ContractTagger
            tagger = ContractTagger()
            logger.info("✓ ContractTagger initialisé avec succès")
            return True
        except ImportError as e:
            logger.error(f"✗ Impossible d'importer ContractTagger: {e}")
            return False
            
    except ImportError as e:
        logger.error(f"✗ Erreur d'import: {e}")
        return False

def main():
    """Fonction principale d'installation"""
    logger.info("🚀 Début de l'installation du Contract Tagger")
    logger.info("=" * 50)
    
    success_steps = 0
    total_steps = 5
    
    # Étape 1: Installation des requirements
    if install_requirements():
        success_steps += 1
    
    # Étape 2: Téléchargement des modèles spaCy
    if download_spacy_models():
        success_steps += 1
    
    # Étape 3: Téléchargement des données NLTK
    if download_nltk_data():
        success_steps += 1
    
    # Étape 4: Création du contrat d'exemple
    if create_sample_contract():
        success_steps += 1
    
    # Étape 5: Test de l'installation
    if test_installation():
        success_steps += 1
    
    # Résumé
    logger.info("=" * 50)
    logger.info(f"Installation terminée: {success_steps}/{total_steps} étapes réussies")
    
    if success_steps == total_steps:
        logger.info("🎉 Installation complète réussie!")
        logger.info("\nPour utiliser le Contract Tagger:")
        logger.info("1. python contract_tagger.py")
        logger.info("2. ou importez ContractTagger dans votre code")
        logger.info("3. Testez avec: python demo_contract_tagger.py")
    else:
        logger.warning("⚠ Installation partiellement réussie. Vérifiez les erreurs ci-dessus.")
    
    return success_steps == total_steps

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)