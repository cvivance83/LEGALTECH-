#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Tagging Automatique par Paragraphe Contractuel
=========================================================

Ce script analyse automatiquement les paragraphes de contrats et leur assigne
des tags appropriés basés sur leur contenu juridique.

Auteur: Assistant IA
Date: 2024
"""

import re
import json
import pandas as pd
import nltk
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pickle
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ContractClauseType(Enum):
    """Types de clauses contractuelles"""
    PARTIES = "parties"
    OBJET = "objet"
    DUREE = "duree"
    PRIX_PAIEMENT = "prix_paiement"
    OBLIGATIONS_VENDEUR = "obligations_vendeur"
    OBLIGATIONS_ACHETEUR = "obligations_acheteur"
    GARANTIES = "garanties"
    RESPONSABILITE = "responsabilite"
    FORCE_MAJEURE = "force_majeure"
    RESILIATION = "resiliation"
    CONFIDENTIALITE = "confidentialite"
    PROPRIETE_INTELLECTUELLE = "propriete_intellectuelle"
    JURISDICTION = "jurisdiction"
    PENALITES = "penalites"
    MODIFICATION = "modification"
    SIGNATURE = "signature"
    ANNEXES = "annexes"
    DIVERS = "divers"

@dataclass
class TaggedParagraph:
    """Représente un paragraphe tagué"""
    text: str
    clause_type: ContractClauseType
    confidence: float
    keywords: List[str]
    article_number: str = ""
    sub_tags: List[str] = None

class ContractTagger:
    """Classe principale pour le tagging automatique de contrats"""
    
    def __init__(self):
        self.patterns = self._load_patterns()
        self.keywords = self._load_keywords()
        self.model = None
        self.vectorizer = None
        self._setup_nlp()
    
    def _setup_nlp(self):
        """Configuration des outils NLP"""
        try:
            # Tentative de chargement du modèle spaCy français
            self.nlp = spacy.load("fr_core_news_sm")
        except OSError:
            logger.warning("Modèle spaCy français non trouvé. Utilisation du modèle par défaut.")
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except OSError:
                logger.error("Aucun modèle spaCy trouvé. Installation requise.")
                self.nlp = None
    
    def _load_patterns(self) -> Dict[ContractClauseType, List[str]]:
        """Charge les patterns regex pour chaque type de clause"""
        return {
            ContractClauseType.PARTIES: [
                r"\b(?:entre|contractant|partie|vendeur|acheteur|client|fournisseur)\b",
                r"\b(?:dénommé|ci-après|représenté par)\b",
                r"\b(?:société|sarl|sas|eurl|sa)\b"
            ],
            ContractClauseType.OBJET: [
                r"\b(?:objet|but|objectif|finalité)\b",
                r"\b(?:présent contrat|présente convention)\b",
                r"\b(?:vente|achat|prestation|service)\b"
            ],
            ContractClauseType.DUREE: [
                r"\b(?:durée|période|terme|échéance|expiration)\b",
                r"\b(?:mois|année|jour|semaine)\b",
                r"\b(?:renouvelable|reconduction|prorogation)\b"
            ],
            ContractClauseType.PRIX_PAIEMENT: [
                r"\b(?:prix|montant|coût|tarif|rémunération)\b",
                r"\b(?:paiement|règlement|versement|échéance)\b",
                r"\b(?:euro|€|\$|devise|tva|ht|ttc)\b",
                r"\b(?:facture|devis|avoir)\b"
            ],
            ContractClauseType.OBLIGATIONS_VENDEUR: [
                r"\b(?:vendeur|fournisseur)\b.*\b(?:s'engage|doit|obligation)\b",
                r"\b(?:livraison|fourniture|mise à disposition)\b",
                r"\b(?:conformité|qualité|spécification)\b"
            ],
            ContractClauseType.OBLIGATIONS_ACHETEUR: [
                r"\b(?:acheteur|client)\b.*\b(?:s'engage|doit|obligation)\b",
                r"\b(?:réception|acceptation|utilisation)\b",
                r"\b(?:coopération|assistance|information)\b"
            ],
            ContractClauseType.GARANTIES: [
                r"\b(?:garantie|garanti|assurance)\b",
                r"\b(?:défaut|vice|conformité)\b",
                r"\b(?:remplacement|réparation|remboursement)\b"
            ],
            ContractClauseType.RESPONSABILITE: [
                r"\b(?:responsabilité|responsable|liable)\b",
                r"\b(?:dommage|préjudice|perte)\b",
                r"\b(?:limitation|exclusion|exonération)\b"
            ],
            ContractClauseType.FORCE_MAJEURE: [
                r"\b(?:force majeure|cas fortuit|événement)\b",
                r"\b(?:imprévisible|irrésistible|extérieur)\b",
                r"\b(?:suspension|report|annulation)\b"
            ],
            ContractClauseType.RESILIATION: [
                r"\b(?:résiliation|résili|rupture|fin)\b",
                r"\b(?:terme|expiration|dénonciation)\b",
                r"\b(?:faute|manquement|inexécution)\b"
            ],
            ContractClauseType.CONFIDENTIALITE: [
                r"\b(?:confidentialité|confidentiel|secret)\b",
                r"\b(?:divulgation|communication|diffusion)\b",
                r"\b(?:information|donnée|document)\b"
            ],
            ContractClauseType.PROPRIETE_INTELLECTUELLE: [
                r"\b(?:propriété intellectuelle|copyright|brevet)\b",
                r"\b(?:marque|logo|invention)\b",
                r"\b(?:droit d'auteur|licence|usage)\b"
            ],
            ContractClauseType.JURISDICTION: [
                r"\b(?:juridiction|tribunal|cour)\b",
                r"\b(?:compétent|ressort|litige)\b",
                r"\b(?:loi applicable|droit|règlement)\b"
            ],
            ContractClauseType.PENALITES: [
                r"\b(?:pénalité|amende|sanction)\b",
                r"\b(?:retard|défaut|manquement)\b",
                r"\b(?:intérêts|dommages)\b"
            ],
            ContractClauseType.MODIFICATION: [
                r"\b(?:modification|amendement|avenant)\b",
                r"\b(?:changement|révision|mise à jour)\b",
                r"\b(?:écrit|accord mutuel)\b"
            ],
            ContractClauseType.SIGNATURE: [
                r"\b(?:signature|signé|signer)\b",
                r"\b(?:exemplaire|original|copie)\b",
                r"\b(?:fait à|le|date)\b"
            ]
        }
    
    def _load_keywords(self) -> Dict[ContractClauseType, List[str]]:
        """Charge les mots-clés pour chaque type de clause"""
        return {
            ContractClauseType.PARTIES: [
                "partie", "contractant", "vendeur", "acheteur", "client", "fournisseur",
                "société", "entreprise", "personne", "morale", "physique"
            ],
            ContractClauseType.OBJET: [
                "objet", "objectif", "but", "finalité", "vente", "achat", "prestation",
                "service", "produit", "bien", "marchandise"
            ],
            ContractClauseType.DUREE: [
                "durée", "période", "terme", "échéance", "mois", "année", "jour",
                "renouvelable", "reconduction", "expiration"
            ],
            ContractClauseType.PRIX_PAIEMENT: [
                "prix", "montant", "coût", "paiement", "règlement", "facture",
                "euro", "devise", "tva", "remise", "acompte"
            ]
        }
    
    def preprocess_text(self, text: str) -> str:
        """Préprocesse le texte pour l'analyse"""
        # Nettoyage de base
        text = re.sub(r'\s+', ' ', text)  # Normalisation des espaces
        text = text.strip()
        
        # Suppression des caractères spéciaux mais conservation de la ponctuation importante
        text = re.sub(r'[^\w\s.,;:!?()-]', '', text)
        
        return text.lower()
    
    def extract_article_number(self, text: str) -> str:
        """Extrait le numéro d'article du paragraphe"""
        patterns = [
            r'article\s+(\d+(?:\.\d+)*)',
            r'art\.?\s+(\d+(?:\.\d+)*)',
            r'^(\d+(?:\.\d+)*)\s*[.-]',
            r'§\s*(\d+(?:\.\d+)*)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                return match.group(1)
        
        return ""
    
    def pattern_based_classification(self, text: str) -> Tuple[ContractClauseType, float]:
        """Classification basée sur les patterns regex"""
        scores = {}
        text_lower = text.lower()
        
        for clause_type, patterns in self.patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, text_lower))
                score += matches
            
            if score > 0:
                scores[clause_type] = score / len(patterns)  # Normalisation
        
        if scores:
            best_type = max(scores, key=scores.get)
            confidence = min(scores[best_type], 1.0)  # Cap à 1.0
            return best_type, confidence
        
        return ContractClauseType.DIVERS, 0.1
    
    def keyword_based_classification(self, text: str) -> Tuple[ContractClauseType, float]:
        """Classification basée sur les mots-clés"""
        scores = {}
        text_words = set(self.preprocess_text(text).split())
        
        for clause_type, keywords in self.keywords.items():
            common_words = text_words.intersection(set(keywords))
            if common_words:
                scores[clause_type] = len(common_words) / len(keywords)
        
        if scores:
            best_type = max(scores, key=scores.get)
            confidence = scores[best_type]
            return best_type, confidence
        
        return ContractClauseType.DIVERS, 0.1
    
    def extract_keywords(self, text: str, clause_type: ContractClauseType) -> List[str]:
        """Extrait les mots-clés pertinents du texte"""
        text_words = set(self.preprocess_text(text).split())
        
        if clause_type in self.keywords:
            relevant_keywords = text_words.intersection(set(self.keywords[clause_type]))
            return list(relevant_keywords)
        
        # Si pas de mots-clés prédéfinis, extraire les mots importants
        if self.nlp:
            doc = self.nlp(text)
            keywords = [token.lemma_ for token in doc 
                       if not token.is_stop and not token.is_punct 
                       and len(token.text) > 3]
            return keywords[:5]  # Top 5 mots-clés
        
        return []
    
    def classify_paragraph(self, text: str) -> TaggedParagraph:
        """Classifie un paragraphe et retourne un objet TaggedParagraph"""
        # Classification par patterns
        pattern_type, pattern_confidence = self.pattern_based_classification(text)
        
        # Classification par mots-clés
        keyword_type, keyword_confidence = self.keyword_based_classification(text)
        
        # Combinaison des résultats (pondération)
        if pattern_confidence > keyword_confidence:
            final_type = pattern_type
            final_confidence = pattern_confidence * 0.7 + keyword_confidence * 0.3
        else:
            final_type = keyword_type
            final_confidence = keyword_confidence * 0.7 + pattern_confidence * 0.3
        
        # Extraction des informations supplémentaires
        article_number = self.extract_article_number(text)
        keywords = self.extract_keywords(text, final_type)
        
        return TaggedParagraph(
            text=text,
            clause_type=final_type,
            confidence=final_confidence,
            keywords=keywords,
            article_number=article_number
        )
    
    def tag_contract(self, contract_text: str) -> List[TaggedParagraph]:
        """Tag un contrat complet en analysant chaque paragraphe"""
        # Division en paragraphes
        paragraphs = self._split_into_paragraphs(contract_text)
        
        tagged_paragraphs = []
        for paragraph in paragraphs:
            if paragraph.strip():  # Ignorer les paragraphes vides
                tagged_paragraph = self.classify_paragraph(paragraph)
                tagged_paragraphs.append(tagged_paragraph)
                
                logger.info(f"Paragraphe tagué: {tagged_paragraph.clause_type.value} "
                           f"(confiance: {tagged_paragraph.confidence:.2f})")
        
        return tagged_paragraphs
    
    def _split_into_paragraphs(self, text: str) -> List[str]:
        """Divise le texte en paragraphes"""
        # Division basique par double saut de ligne
        paragraphs = re.split(r'\n\s*\n', text)
        
        # Division alternative par articles
        if len(paragraphs) == 1:
            paragraphs = re.split(r'(?=Article\s+\d+|Art\.?\s*\d+)', text, flags=re.IGNORECASE)
        
        return [p.strip() for p in paragraphs if p.strip()]
    
    def export_tags_to_json(self, tagged_paragraphs: List[TaggedParagraph], 
                           filename: str = "contract_tags.json"):
        """Exporte les tags vers un fichier JSON"""
        data = []
        for tp in tagged_paragraphs:
            data.append({
                "text": tp.text,
                "clause_type": tp.clause_type.value,
                "confidence": tp.confidence,
                "keywords": tp.keywords,
                "article_number": tp.article_number
            })
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Tags exportés vers {filename}")
    
    def export_tags_to_excel(self, tagged_paragraphs: List[TaggedParagraph], 
                            filename: str = "contract_tags.xlsx"):
        """Exporte les tags vers un fichier Excel"""
        data = []
        for tp in tagged_paragraphs:
            data.append({
                "Texte": tp.text,
                "Type de Clause": tp.clause_type.value,
                "Confiance": tp.confidence,
                "Mots-clés": ", ".join(tp.keywords),
                "Article": tp.article_number
            })
        
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False, engine='openpyxl')
        
        logger.info(f"Tags exportés vers {filename}")
    
    def generate_summary(self, tagged_paragraphs: List[TaggedParagraph]) -> Dict[str, Any]:
        """Génère un résumé de l'analyse du contrat"""
        clause_counts = {}
        total_confidence = 0
        
        for tp in tagged_paragraphs:
            clause_type = tp.clause_type.value
            clause_counts[clause_type] = clause_counts.get(clause_type, 0) + 1
            total_confidence += tp.confidence
        
        avg_confidence = total_confidence / len(tagged_paragraphs) if tagged_paragraphs else 0
        
        return {
            "total_paragraphs": len(tagged_paragraphs),
            "clause_distribution": clause_counts,
            "average_confidence": avg_confidence,
            "most_common_clause": max(clause_counts, key=clause_counts.get) if clause_counts else None
        }

def main():
    """Fonction principale pour démonstration"""
    # Exemple d'utilisation
    tagger = ContractTagger()
    
    # Texte de contrat exemple
    sample_contract = """
    Article 1 - Parties
    Entre la société ABC SARL, représentée par son gérant Monsieur Dupont,
    ci-après dénommée "le Vendeur", et la société XYZ SA, représentée par
    sa directrice Madame Martin, ci-après dénommée "l'Acheteur".
    
    Article 2 - Objet
    Le présent contrat a pour objet la vente de matériel informatique
    selon les spécifications définies en annexe.
    
    Article 3 - Prix et Paiement
    Le prix total de la vente s'élève à 50 000 euros HT.
    Le paiement sera effectué en trois versements égaux.
    
    Article 4 - Garanties
    Le vendeur garantit la conformité du matériel livré pendant une
    période de 24 mois à compter de la livraison.
    
    Article 5 - Résiliation
    En cas de manquement grave aux obligations contractuelles,
    le contrat pourra être résilié de plein droit.
    """
    
    # Analyse du contrat
    print("Analyse du contrat en cours...")
    tagged_paragraphs = tagger.tag_contract(sample_contract)
    
    # Affichage des résultats
    print("\n=== RÉSULTATS DU TAGGING ===")
    for tp in tagged_paragraphs:
        print(f"\nType: {tp.clause_type.value}")
        print(f"Confiance: {tp.confidence:.2f}")
        print(f"Article: {tp.article_number}")
        print(f"Mots-clés: {', '.join(tp.keywords)}")
        print(f"Texte: {tp.text[:100]}...")
    
    # Génération du résumé
    summary = tagger.generate_summary(tagged_paragraphs)
    print(f"\n=== RÉSUMÉ ===")
    print(f"Nombre total de paragraphes: {summary['total_paragraphs']}")
    print(f"Confiance moyenne: {summary['average_confidence']:.2f}")
    print(f"Distribution des clauses: {summary['clause_distribution']}")
    
    # Export des résultats
    tagger.export_tags_to_json(tagged_paragraphs)
    print("\nRésultats exportés vers contract_tags.json")

if __name__ == "__main__":
    main()