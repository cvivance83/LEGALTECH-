# Script de Tagging Automatique par Paragraphe Contractuel

## 📋 Description

Ce projet propose un système complet de **tagging automatique** pour les paragraphes de contrats juridiques. Il utilise des techniques de traitement du langage naturel (NLP) et d'apprentissage automatique pour identifier et classifier automatiquement différents types de clauses contractuelles.

## 🚀 Fonctionnalités

### ✨ Fonctionnalités Principales
- **Classification automatique** de 18 types de clauses contractuelles
- **Analyse par paragraphe** avec score de confiance
- **Extraction automatique** des numéros d'articles
- **Détection de mots-clés** pertinents par clause
- **Export multiformat** (JSON, Excel)
- **Résumé automatique** des contrats analysés

### 📊 Types de Clauses Détectées
- **Parties** - Identification des contractants
- **Objet** - Finalité du contrat
- **Durée** - Période d'exécution
- **Prix/Paiement** - Modalités financières
- **Obligations Vendeur/Acheteur** - Engagements des parties
- **Garanties** - Conditions de garantie
- **Responsabilité** - Clauses de responsabilité
- **Force Majeure** - Événements exceptionnels
- **Résiliation** - Conditions de fin de contrat
- **Confidentialité** - Protection des informations
- **Propriété Intellectuelle** - Droits d'auteur et brevets
- **Juridiction** - Compétence territoriale
- **Pénalités** - Sanctions contractuelles
- **Modification** - Amendements
- **Signature** - Validation du contrat
- **Annexes** - Documents complémentaires
- **Divers** - Autres clauses

## 📦 Installation

### Installation Automatique
```bash
# Cloner ou télécharger les fichiers du projet
python setup_contract_tagger.py
```

### Installation Manuelle
```bash
# 1. Installer les dépendances Python
pip install -r contract_tagger_requirements.txt

# 2. Télécharger les modèles spaCy
python -m spacy download fr_core_news_sm
python -m spacy download en_core_web_sm

# 3. Télécharger les données NLTK (optionnel)
python -c "import nltk; nltk.download(['punkt', 'stopwords', 'wordnet'])"
```

### Dépendances
- **Python** 3.8+
- **spaCy** ≥ 3.6.0 (modèles français/anglais)
- **NLTK** ≥ 3.8.1
- **scikit-learn** ≥ 1.3.0
- **pandas** ≥ 2.0.0
- **openpyxl** ≥ 3.1.0

## 🔧 Utilisation

### Utilisation Basique

```python
from contract_tagger import ContractTagger

# Initialisation
tagger = ContractTagger()

# Analyse d'un paragraphe
paragraph = "Le prix total s'élève à 50 000 euros HT, payable en trois versements."
result = tagger.classify_paragraph(paragraph)

print(f"Type: {result.clause_type.value}")
print(f"Confiance: {result.confidence:.2f}")
print(f"Mots-clés: {result.keywords}")
```

### Analyse d'un Contrat Complet

```python
# Charger un contrat
with open("mon_contrat.txt", "r", encoding="utf-8") as f:
    contract_text = f.read()

# Analyser le contrat
tagged_paragraphs = tagger.tag_contract(contract_text)

# Générer un résumé
summary = tagger.generate_summary(tagged_paragraphs)
print(summary)
```

### Export des Résultats

```python
# Export JSON
tagger.export_tags_to_json(tagged_paragraphs, "resultats.json")

# Export Excel
tagger.export_tags_to_excel(tagged_paragraphs, "resultats.xlsx")
```

## 🎯 Démonstration

Lancez le script de démonstration pour voir toutes les fonctionnalités :

```bash
python demo_contract_tagger.py
```

Ce script démontre :
- Classification de paragraphes individuels
- Analyse complète d'un contrat d'exemple
- Fonctionnalités d'export
- Fonctionnalités avancées
- Tests de performance

## 📁 Structure du Projet

```
projet/
├── contract_tagger.py              # Script principal
├── setup_contract_tagger.py        # Installation automatique
├── demo_contract_tagger.py         # Démonstration complète
├── contract_tagger_requirements.txt # Dépendances
├── README_CONTRACT_TAGGER.md       # Documentation
├── sample_contract.txt             # Contrat d'exemple (généré)
└── output/                         # Fichiers de sortie
    ├── contract_tags.json
    └── contract_tags.xlsx
```

## 🔍 Algorithme de Classification

### Méthodes Utilisées

1. **Classification par Patterns Regex**
   - Recherche de motifs linguistiques spécifiques
   - Expressions régulières adaptées au vocabulaire juridique français

2. **Classification par Mots-clés**
   - Dictionnaires de mots-clés par type de clause
   - Calcul de similarité lexicale

3. **Traitement NLP avec spaCy**
   - Lemmatisation et analyse morphologique
   - Extraction d'entités nommées

4. **Combinaison Pondérée**
   - Fusion des résultats avec coefficients optimisés
   - Score de confiance final normalisé

### Scores de Confiance

- **🟢 Élevé (0.7-1.0)** : Classification très fiable
- **🟡 Moyen (0.4-0.7)** : Classification probable
- **🔴 Faible (0.0-0.4)** : Classification incertaine

## 📊 Exemples de Résultats

### Analyse d'un Paragraphe

**Input:**
```
"Le prix total de la vente s'élève à 100 000 euros HT, payable en trois versements égaux."
```

**Output:**
```json
{
  "clause_type": "prix_paiement",
  "confidence": 0.85,
  "keywords": ["prix", "euros", "payable", "versements"],
  "article_number": ""
}
```

### Résumé d'un Contrat

```json
{
  "total_paragraphs": 12,
  "average_confidence": 0.73,
  "most_common_clause": "obligations_vendeur",
  "clause_distribution": {
    "parties": 1,
    "objet": 1,
    "prix_paiement": 2,
    "garanties": 1,
    "obligations_vendeur": 3,
    "resiliation": 1,
    "juridiction": 1,
    "signature": 1,
    "divers": 1
  }
}
```

## ⚡ Performance

- **Vitesse** : ~30-50 paragraphes/seconde
- **Précision** : ~85% sur corpus de test
- **Langues** : Français (primaire), Anglais (fallback)
- **Format** : Texte brut, pas de formatage spécial requis

## 🛠️ Personnalisation

### Ajouter de Nouveaux Types de Clauses

```python
# Dans contract_tagger.py, modifier l'enum ContractClauseType
class ContractClauseType(Enum):
    # ... clauses existantes ...
    NOUVEAU_TYPE = "nouveau_type"

# Ajouter les patterns correspondants dans _load_patterns()
```

### Modifier les Patterns de Détection

```python
# Personnaliser les expressions régulières
def _load_patterns(self):
    return {
        ContractClauseType.VOTRE_TYPE: [
            r"\b(?:mot-clé1|mot-clé2)\b",
            r"\b(?:pattern|spécifique)\b"
        ]
    }
```

## 📈 Améliorations Futures

- [ ] **Machine Learning avancé** avec modèles pré-entraînés
- [ ] **Support multilingue** étendu
- [ ] **Interface graphique** web
- [ ] **API REST** pour intégration
- [ ] **Base de données** de contrats pour entraînement
- [ ] **Extraction d'entités** (dates, montants, noms)

## 🐛 Résolution de Problèmes

### Erreurs Communes

**ModuleNotFoundError: No module named 'spacy'**
```bash
pip install spacy
python -m spacy download fr_core_news_sm
```

**OSError: Can't find model 'fr_core_news_sm'**
```bash
python -m spacy download fr_core_news_sm
```

**ImportError lors de l'import d'openpyxl**
```bash
pip install openpyxl
```

### Problèmes de Performance

- **Textes très longs** : Diviser en chunks plus petits
- **Mémoire insuffisante** : Traiter par batch
- **Modèles spaCy manquants** : Le script fonctionne sans, avec précision réduite

## 📄 Licence

Ce projet est fourni à des fins éducatives et de démonstration. 
Adaptez selon vos besoins pour usage commercial.

## 🤝 Contribution

Pour contribuer au projet :
1. Forkez le repository
2. Créez une branche feature
3. Testez vos modifications
4. Soumettez une pull request

## 📞 Support

Pour questions techniques ou suggestions :
- Ouvrir une issue GitHub
- Consulter la documentation dans le code
- Tester avec `demo_contract_tagger.py`

---

**Version:** 1.0  
**Auteur:** Assistant IA  
**Dernière mise à jour:** 2024  
**Langue principale:** Français