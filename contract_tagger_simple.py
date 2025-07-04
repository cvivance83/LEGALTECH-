#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Tagging Automatique par Paragraphe Contractuel (Version Simplifiée)
=============================================================================

Version simplifiée qui fonctionne uniquement avec les librairies Python standard.

Usage: python3 contract_tagger_simple.py
"""

import re
import json
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from enum import Enum
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
    JURISDICTION = "juridiction"
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

class SimpleContractTagger:
    """Version simplifiée du tagger de contrats"""
    
    def __init__(self):
        self.patterns = self._load_patterns()
        self.keywords = self._load_keywords()
        self.stop_words = self._get_french_stop_words()
    
    def _get_french_stop_words(self) -> set:
        """Mots vides français basiques"""
        return {
            'le', 'la', 'les', 'un', 'une', 'des', 'du', 'de', 'et', 'ou', 'à', 'au',
            'aux', 'avec', 'sans', 'sous', 'sur', 'dans', 'par', 'pour', 'entre',
            'contre', 'vers', 'chez', 'pendant', 'avant', 'après', 'depuis', 'jusqu',
            'car', 'donc', 'mais', 'or', 'ni', 'cependant', 'néanmoins', 'toutefois',
            'ce', 'cette', 'ces', 'cet', 'son', 'sa', 'ses', 'leur', 'leurs', 'notre',
            'nos', 'votre', 'vos', 'mon', 'ma', 'mes', 'il', 'elle', 'ils', 'elles',
            'je', 'tu', 'nous', 'vous', 'qui', 'que', 'quoi', 'dont', 'où', 'quand',
            'comment', 'pourquoi', 'si', 'comme', 'bien', 'très', 'plus', 'moins',
            'aussi', 'encore', 'déjà', 'jamais', 'toujours', 'souvent', 'parfois'
        }
    
    def _load_patterns(self) -> Dict[ContractClauseType, List[str]]:
        """Charge les patterns regex pour chaque type de clause"""
        return {
            ContractClauseType.PARTIES: [
                r'\b(?:entre|contractant|partie|vendeur|acheteur|client|fournisseur)\b',
                r'\b(?:dénommé|ci-après|représenté par)\b',
                r'\b(?:société|sarl|sas|eurl|sa)\b'
            ],
            ContractClauseType.OBJET: [
                r'\b(?:objet|but|objectif|finalité)\b',
                r'\b(?:présent contrat|présente convention)\b',
                r'\b(?:vente|achat|prestation|service)\b'
            ],
            ContractClauseType.DUREE: [
                r'\b(?:durée|période|terme|échéance|expiration)\b',
                r'\b(?:mois|année|jour|semaine)\b',
                r'\b(?:renouvelable|reconduction|prorogation)\b'
            ],
            ContractClauseType.PRIX_PAIEMENT: [
                r'\b(?:prix|montant|coût|tarif|rémunération)\b',
                r'\b(?:paiement|règlement|versement|échéance)\b',
                r'\b(?:euro|€|\$|devise|tva|ht|ttc)\b',
                r'\b(?:facture|devis|avoir)\b'
            ],
            ContractClauseType.OBLIGATIONS_VENDEUR: [
                r'\b(?:vendeur|fournisseur)\b.*\b(?:s\'engage|doit|obligation)\b',
                r'\b(?:livraison|fourniture|mise à disposition)\b',
                r'\b(?:conformité|qualité|spécification)\b'
            ],
            ContractClauseType.OBLIGATIONS_ACHETEUR: [
                r'\b(?:acheteur|client)\b.*\b(?:s\'engage|doit|obligation)\b',
                r'\b(?:réception|acceptation|utilisation)\b',
                r'\b(?:coopération|assistance|information)\b'
            ],
            ContractClauseType.GARANTIES: [
                r'\b(?:garantie|garanti|assurance)\b',
                r'\b(?:défaut|vice|conformité)\b',
                r'\b(?:remplacement|réparation|remboursement)\b'
            ],
            ContractClauseType.RESPONSABILITE: [
                r'\b(?:responsabilité|responsable)\b',
                r'\b(?:dommage|préjudice|perte)\b',
                r'\b(?:limitation|exclusion|exonération)\b'
            ],
            ContractClauseType.FORCE_MAJEURE: [
                r'\b(?:force majeure|cas fortuit|événement)\b',
                r'\b(?:imprévisible|irrésistible|extérieur)\b',
                r'\b(?:suspension|report|annulation)\b'
            ],
            ContractClauseType.RESILIATION: [
                r'\b(?:résiliation|résili|rupture|fin)\b',
                r'\b(?:terme|expiration|dénonciation)\b',
                r'\b(?:faute|manquement|inexécution)\b'
            ],
            ContractClauseType.CONFIDENTIALITE: [
                r'\b(?:confidentialité|confidentiel|secret)\b',
                r'\b(?:divulgation|communication|diffusion)\b',
                r'\b(?:information|donnée|document)\b'
            ],
            ContractClauseType.PROPRIETE_INTELLECTUELLE: [
                r'\b(?:propriété intellectuelle|copyright|brevet)\b',
                r'\b(?:marque|logo|invention)\b',
                r'\b(?:droit d\'auteur|licence|usage)\b'
            ],
            ContractClauseType.JURISDICTION: [
                r'\b(?:juridiction|tribunal|cour)\b',
                r'\b(?:compétent|ressort|litige)\b',
                r'\b(?:loi applicable|droit|règlement)\b'
            ],
            ContractClauseType.PENALITES: [
                r'\b(?:pénalité|amende|sanction)\b',
                r'\b(?:retard|défaut|manquement)\b',
                r'\b(?:intérêts|dommages)\b'
            ],
            ContractClauseType.MODIFICATION: [
                r'\b(?:modification|amendement|avenant)\b',
                r'\b(?:changement|révision|mise à jour)\b',
                r'\b(?:écrit|accord mutuel)\b'
            ],
            ContractClauseType.SIGNATURE: [
                r'\b(?:signature|signé|signer)\b',
                r'\b(?:exemplaire|original|copie)\b',
                r'\b(?:fait à|le|date)\b'
            ]
        }
    
    def _load_keywords(self) -> Dict[ContractClauseType, List[str]]:
        """Charge les mots-clés pour chaque type de clause"""
        return {
            ContractClauseType.PARTIES: [
                "partie", "contractant", "vendeur", "acheteur", "client", "fournisseur",
                "société", "entreprise", "personne", "morale", "physique", "sarl", "sa"
            ],
            ContractClauseType.OBJET: [
                "objet", "objectif", "but", "finalité", "vente", "achat", "prestation",
                "service", "produit", "bien", "marchandise", "contrat"
            ],
            ContractClauseType.DUREE: [
                "durée", "période", "terme", "échéance", "mois", "année", "jour",
                "renouvelable", "reconduction", "expiration"
            ],
            ContractClauseType.PRIX_PAIEMENT: [
                "prix", "montant", "coût", "paiement", "règlement", "facture",
                "euro", "devise", "tva", "remise", "acompte", "versement"
            ],
            ContractClauseType.GARANTIES: [
                "garantie", "garanti", "défaut", "vice", "conformité", "réparation"
            ],
            ContractClauseType.RESILIATION: [
                "résiliation", "rupture", "fin", "terme", "manquement", "faute"
            ],
            ContractClauseType.CONFIDENTIALITE: [
                "confidentialité", "confidentiel", "secret", "divulgation", "information"
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
    
    def extract_keywords(self, text: str, max_keywords: int = 5) -> List[str]:
        """Extrait les mots-clés du texte"""
        words = re.findall(r'\b\w+\b', self.preprocess_text(text))
        
        # Filtrer les mots vides et les mots courts
        filtered_words = [
            word for word in words 
            if len(word) > 3 and word not in self.stop_words
        ]
        
        # Compter les occurrences
        word_count = {}
        for word in filtered_words:
            word_count[word] = word_count.get(word, 0) + 1
        
        # Trier par fréquence et retourner le top
        sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
        return [word for word, count in sorted_words[:max_keywords]]
    
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
        keywords = self.extract_keywords(text)
        
        return TaggedParagraph(
            text=text,
            clause_type=final_type,
            confidence=final_confidence,
            keywords=keywords,
            article_number=article_number
        )
    
    def split_into_paragraphs(self, text: str) -> List[str]:
        """Divise le texte en paragraphes"""
        # Division basique par double saut de ligne
        paragraphs = re.split(r'\n\s*\n', text)
        
        # Division alternative par articles
        if len(paragraphs) == 1:
            paragraphs = re.split(r'(?=Article\s+\d+|Art\.?\s*\d+)', text, flags=re.IGNORECASE)
        
        return [p.strip() for p in paragraphs if p.strip()]
    
    def tag_contract(self, contract_text: str) -> List[TaggedParagraph]:
        """Tag un contrat complet en analysant chaque paragraphe"""
        # Division en paragraphes
        paragraphs = self.split_into_paragraphs(contract_text)
        
        tagged_paragraphs = []
        for paragraph in paragraphs:
            if paragraph.strip():  # Ignorer les paragraphes vides
                tagged_paragraph = self.classify_paragraph(paragraph)
                tagged_paragraphs.append(tagged_paragraph)
                
                logger.info(f"Paragraphe tagué: {tagged_paragraph.clause_type.value} "
                           f"(confiance: {tagged_paragraph.confidence:.2f})")
        
        return tagged_paragraphs
    
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
    print("🎯 DÉMONSTRATION DU CONTRACT TAGGER SIMPLIFIÉ")
    print("=" * 55)
    
    # Exemple d'utilisation
    tagger = SimpleContractTagger()
    
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
    
    Article 6 - Confidentialité
    Les informations échangées dans le cadre de ce contrat 
    resteront strictement confidentielles.
    """
    
    # Analyse du contrat
    print("📄 Analyse du contrat en cours...")
    tagged_paragraphs = tagger.tag_contract(sample_contract)
    
    # Affichage des résultats
    print(f"\n📊 RÉSULTATS DU TAGGING ({len(tagged_paragraphs)} paragraphes)")
    print("=" * 55)
    
    for i, tp in enumerate(tagged_paragraphs, 1):
        confidence_emoji = "🟢" if tp.confidence > 0.7 else "🟡" if tp.confidence > 0.4 else "🔴"
        print(f"\n{i}. {confidence_emoji} Article {tp.article_number or 'N/A'}")
        print(f"   Type: {tp.clause_type.value}")
        print(f"   Confiance: {tp.confidence:.2f}")
        print(f"   Mots-clés: {', '.join(tp.keywords) if tp.keywords else 'Aucun'}")
        print(f"   Extrait: {tp.text[:100]}...")
    
    # Génération du résumé
    summary = tagger.generate_summary(tagged_paragraphs)
    print(f"\n📈 RÉSUMÉ DE L'ANALYSE")
    print("=" * 55)
    print(f"• Nombre total de paragraphes: {summary['total_paragraphs']}")
    print(f"• Confiance moyenne: {summary['average_confidence']:.2f}")
    print(f"• Type le plus fréquent: {summary['most_common_clause']}")
    print(f"• Distribution des clauses:")
    for clause_type, count in summary['clause_distribution'].items():
        print(f"  - {clause_type}: {count}")
    
    # Export des résultats
    tagger.export_tags_to_json(tagged_paragraphs, "demo_tags.json")
    print(f"\n💾 Résultats exportés vers 'demo_tags.json'")
    
    print(f"\n✅ Analyse terminée avec succès!")

if __name__ == "__main__":
    main()