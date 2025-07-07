#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Démonstration du Script de Tagging Automatique de Contrats
===========================================================

Ce script démontre l'utilisation complète du Contract Tagger avec
plusieurs exemples de contrats et toutes les fonctionnalités disponibles.

Usage: python demo_contract_tagger.py
"""

import os
import json
from contract_tagger import ContractTagger, ContractClauseType
import logging

# Configuration du logging pour la démo
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def demo_basic_usage():
    """Démonstration de l'utilisation de base"""
    print("=" * 60)
    print("🔍 DÉMONSTRATION - UTILISATION DE BASE")
    print("=" * 60)
    
    # Initialisation du tagger
    tagger = ContractTagger()
    
    # Exemples de paragraphes individuels
    test_paragraphs = [
        "Entre la société ABC SARL, représentée par son gérant, et la société XYZ SA, il est convenu ce qui suit.",
        "Le présent contrat a pour objet la vente de matériel informatique selon les spécifications définies.",
        "Le prix total s'élève à 50 000 euros HT, payable en trois versements égaux.",
        "Le vendeur garantit la conformité du matériel pendant 24 mois.",
        "En cas de manquement grave, le contrat pourra être résilié de plein droit.",
        "Les informations échangées resteront strictement confidentielles."
    ]
    
    print("\n📝 Analyse de paragraphes individuels:")
    for i, paragraph in enumerate(test_paragraphs, 1):
        tagged = tagger.classify_paragraph(paragraph)
        print(f"\n{i}. Paragraphe: {paragraph[:50]}...")
        print(f"   Type détecté: {tagged.clause_type.value}")
        print(f"   Confiance: {tagged.confidence:.2f}")
        print(f"   Mots-clés: {', '.join(tagged.keywords)}")

def demo_full_contract_analysis():
    """Démonstration de l'analyse d'un contrat complet"""
    print("\n" + "=" * 60)
    print("📄 DÉMONSTRATION - ANALYSE CONTRAT COMPLET")
    print("=" * 60)
    
    tagger = ContractTagger()
    
    # Vérifier si le fichier d'exemple existe
    if os.path.exists("sample_contract.txt"):
        with open("sample_contract.txt", "r", encoding="utf-8") as f:
            contract_text = f.read()
        
        print("\n📖 Analyse du contrat d'exemple...")
        tagged_paragraphs = tagger.tag_contract(contract_text)
        
        # Affichage des résultats détaillés
        print(f"\n📊 Résultats de l'analyse ({len(tagged_paragraphs)} paragraphes):")
        
        for i, tp in enumerate(tagged_paragraphs, 1):
            print(f"\n--- Paragraphe {i} ---")
            print(f"Article: {tp.article_number or 'Non spécifié'}")
            print(f"Type: {tp.clause_type.value}")
            print(f"Confiance: {tp.confidence:.2f}")
            print(f"Mots-clés: {', '.join(tp.keywords) if tp.keywords else 'Aucun'}")
            print(f"Extrait: {tp.text[:100]}...")
        
        # Génération du résumé
        summary = tagger.generate_summary(tagged_paragraphs)
        print(f"\n📈 RÉSUMÉ DE L'ANALYSE:")
        print(f"- Nombre total de paragraphes: {summary['total_paragraphs']}")
        print(f"- Confiance moyenne: {summary['average_confidence']:.2f}")
        print(f"- Type de clause le plus fréquent: {summary['most_common_clause']}")
        print(f"- Distribution des clauses:")
        for clause_type, count in summary['clause_distribution'].items():
            print(f"  • {clause_type}: {count}")
        
        return tagged_paragraphs
    else:
        print("❌ Fichier sample_contract.txt non trouvé. Exécutez d'abord setup_contract_tagger.py")
        return []

def demo_export_features(tagged_paragraphs):
    """Démonstration des fonctionnalités d'export"""
    if not tagged_paragraphs:
        return
    
    print("\n" + "=" * 60)
    print("💾 DÉMONSTRATION - FONCTIONNALITÉS D'EXPORT")
    print("=" * 60)
    
    tagger = ContractTagger()
    
    # Export JSON
    print("\n📄 Export vers JSON...")
    tagger.export_tags_to_json(tagged_paragraphs, "demo_contract_tags.json")
    
    # Vérification du fichier JSON créé
    if os.path.exists("demo_contract_tags.json"):
        with open("demo_contract_tags.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"✓ Fichier JSON créé avec {len(data)} entrées")
        
        # Affichage d'un exemple
        if data:
            print("\n📋 Exemple d'entrée JSON:")
            example = data[0]
            print(json.dumps(example, indent=2, ensure_ascii=False)[:300] + "...")
    
    # Export Excel
    print("\n📊 Export vers Excel...")
    try:
        tagger.export_tags_to_excel(tagged_paragraphs, "demo_contract_tags.xlsx")
        if os.path.exists("demo_contract_tags.xlsx"):
            print("✓ Fichier Excel créé avec succès")
        else:
            print("❌ Erreur lors de la création du fichier Excel")
    except Exception as e:
        print(f"❌ Erreur Excel: {e}")

def demo_advanced_features():
    """Démonstration des fonctionnalités avancées"""
    print("\n" + "=" * 60)
    print("🔧 DÉMONSTRATION - FONCTIONNALITÉS AVANCÉES")
    print("=" * 60)
    
    tagger = ContractTagger()
    
    print("\n🎯 Test de détection de numéros d'articles:")
    article_examples = [
        "Article 1 - Définitions",
        "Art. 2.1 - Obligations générales",
        "§ 3 - Modalités de paiement",
        "5.2 - Clause de résiliation"
    ]
    
    for example in article_examples:
        article_num = tagger.extract_article_number(example)
        print(f"  '{example}' → Article: {article_num or 'Non détecté'}")
    
    print("\n🔍 Test de préprocessing de texte:")
    messy_text = "  Article   1   -    PARTIES   \n\n  Entre  la  société  "
    clean_text = tagger.preprocess_text(messy_text)
    print(f"  Avant: '{messy_text}'")
    print(f"  Après: '{clean_text}'")
    
    print("\n📊 Types de clauses disponibles:")
    for clause_type in ContractClauseType:
        print(f"  • {clause_type.value}")

def demo_custom_contract():
    """Démonstration avec un contrat personnalisé"""
    print("\n" + "=" * 60)
    print("✏️ DÉMONSTRATION - CONTRAT PERSONNALISÉ")
    print("=" * 60)
    
    # Contrat de service personnalisé
    custom_contract = """
    CONTRAT DE PRESTATION DE SERVICES
    
    Article 1 - Identification des parties
    Entre Monsieur Pierre DURAND, consultant indépendant, domicilié au 15 rue Victor Hugo, 
    75016 Paris, ci-après dénommé "le Prestataire",
    
    Et la société INNOVATION TECH, SARL au capital de 100 000 euros, sise 25 boulevard 
    Haussmann, 75009 Paris, représentée par Madame Sophie LEBLANC, ci-après dénommée "le Client".
    
    Article 2 - Mission
    Le présent contrat a pour objet la réalisation d'une mission de conseil en transformation 
    digitale comprenant l'audit des processus existants et la recommandation de solutions.
    
    Article 3 - Durée et planning
    La mission se déroulera sur une période de 6 mois à compter du 1er janvier 2024, 
    avec possibilité de prolongation sur accord mutuel des parties.
    
    Article 4 - Rémunération
    La rémunération du Prestataire est fixée à 500 euros par jour de prestation, 
    soit un montant total estimé de 60 000 euros HT pour l'ensemble de la mission.
    
    Article 5 - Propriété intellectuelle
    Tous les développements, créations et améliorations réalisés dans le cadre de cette 
    mission demeurent la propriété exclusive du Client.
    
    Article 6 - Clause de non-divulgation
    Le Prestataire s'engage à ne divulguer aucune information confidentielle du Client 
    pendant la durée du contrat et pendant 3 ans après sa fin.
    """
    
    tagger = ContractTagger()
    
    print("\n🔄 Analyse en cours du contrat de service...")
    tagged_paragraphs = tagger.tag_contract(custom_contract)
    
    print(f"\n📋 Résultats pour le contrat de service ({len(tagged_paragraphs)} paragraphes):")
    
    # Groupement par type de clause
    clause_groups = {}
    for tp in tagged_paragraphs:
        clause_type = tp.clause_type.value
        if clause_type not in clause_groups:
            clause_groups[clause_type] = []
        clause_groups[clause_type].append(tp)
    
    for clause_type, paragraphs in clause_groups.items():
        print(f"\n📌 {clause_type.upper()} ({len(paragraphs)} paragraphe(s)):")
        for tp in paragraphs:
            confidence_indicator = "🟢" if tp.confidence > 0.7 else "🟡" if tp.confidence > 0.4 else "🔴"
            print(f"  {confidence_indicator} Confiance: {tp.confidence:.2f} | {tp.text[:80]}...")

def run_performance_test():
    """Test de performance avec multiple contrats"""
    print("\n" + "=" * 60)
    print("⚡ TEST DE PERFORMANCE")
    print("=" * 60)
    
    import time
    
    tagger = ContractTagger()
    
    # Simulation de multiples contrats
    test_contracts = [
        "Article 1 - Les parties contractantes sont définies comme suit...",
        "Le prix de vente est fixé à 25 000 euros, payable comptant...",
        "La garantie couvre tous les défauts de fabrication pendant 12 mois...",
        "En cas de litige, les tribunaux de Paris seront compétents...",
        "La résiliation peut intervenir en cas de manquement grave..."
    ] * 10  # 50 paragraphes au total
    
    print(f"📊 Test avec {len(test_contracts)} paragraphes...")
    
    start_time = time.time()
    results = []
    
    for contract in test_contracts:
        tagged = tagger.classify_paragraph(contract)
        results.append(tagged)
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"⏱️ Temps d'exécution: {duration:.2f} secondes")
    print(f"🚀 Vitesse: {len(test_contracts)/duration:.1f} paragraphes/seconde")
    
    # Analyse de la distribution des résultats
    clause_distribution = {}
    total_confidence = 0
    
    for result in results:
        clause_type = result.clause_type.value
        clause_distribution[clause_type] = clause_distribution.get(clause_type, 0) + 1
        total_confidence += result.confidence
    
    avg_confidence = total_confidence / len(results)
    print(f"📈 Confiance moyenne: {avg_confidence:.2f}")
    print(f"📊 Distribution: {clause_distribution}")

def main():
    """Fonction principale de démonstration"""
    print("🎯 DÉMONSTRATION COMPLÈTE DU CONTRACT TAGGER")
    print("Version: 1.0 | Auteur: Assistant IA")
    
    try:
        # 1. Utilisation de base
        demo_basic_usage()
        
        # 2. Analyse complète d'un contrat
        tagged_paragraphs = demo_full_contract_analysis()
        
        # 3. Fonctionnalités d'export
        demo_export_features(tagged_paragraphs)
        
        # 4. Fonctionnalités avancées
        demo_advanced_features()
        
        # 5. Contrat personnalisé
        demo_custom_contract()
        
        # 6. Test de performance
        run_performance_test()
        
        print("\n" + "=" * 60)
        print("✅ DÉMONSTRATION TERMINÉE AVEC SUCCÈS!")
        print("=" * 60)
        
        print("\n📁 Fichiers générés:")
        files_created = []
        if os.path.exists("demo_contract_tags.json"):
            files_created.append("demo_contract_tags.json")
        if os.path.exists("demo_contract_tags.xlsx"):
            files_created.append("demo_contract_tags.xlsx")
        
        if files_created:
            for file in files_created:
                file_size = os.path.getsize(file)
                print(f"  📄 {file} ({file_size} bytes)")
        else:
            print("  Aucun fichier d'export généré")
        
        print("\n🚀 Pour utiliser le Contract Tagger dans votre projet:")
        print("  from contract_tagger import ContractTagger")
        print("  tagger = ContractTagger()")
        print("  results = tagger.tag_contract(your_contract_text)")
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        print("💡 Solution: Exécutez d'abord 'python setup_contract_tagger.py'")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()