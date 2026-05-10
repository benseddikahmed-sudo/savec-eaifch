[README (6).md](https://github.com/user-attachments/files/27570288/README.6.md)
# SAVEC × EAIFCH 2.0

**Statistical Architecture for Validated Ethical Curation**
× **Ethical AI Framework for Cultural Heritage, v2.0**

[![DOI](https://img.shields.io/badge/DOI-10.17605%2FOSF.IO%2FY8VBU-blue)](https://doi.org/10.17605/OSF.IO/Y8VBU)
[![OSF](https://img.shields.io/badge/OSF-osf.io%2Fy8vbu-teal)](https://osf.io/y8vbu)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Status: Prototype](https://img.shields.io/badge/Status-Prototype-orange)]()
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue)]()

> *"Maximum community authority with minimum computational privilege."*

---

## En une phrase

Ce projet propose une architecture logicielle pour que les institutions culturelles
puissent utiliser l'IA sur des matériaux patrimoniaux **sans se faire dépasser par
elle** — en validant statistiquement avant de décider, en faisant gouverner les
communautés, et en gardant l'humain dans la boucle.

---

## Table des matières

1. [Contexte et motivation](#1-contexte-et-motivation)
2. [Deux fichiers, une architecture](#2-deux-fichiers-une-architecture)
3. [Installation en 2 minutes](#3-installation-en-2-minutes)
4. [Démarrage rapide](#4-démarrage-rapide)
5. [Structure des modules](#5-structure-des-modules)
6. [Points d'entrée principaux](#6-points-dentrée-principaux)
7. [Flux de données complet](#7-flux-de-données-complet)
8. [État d'avancement](#8-état-davancement)
9. [Documentation](#9-documentation)
10. [Citation](#10-citation)
11. [Auteur et contact](#11-auteur-et-contact)

---

## 1. Contexte et motivation

Les humanités numériques utilisent de plus en plus des LLMs (grands modèles de
langage) sur des matériaux patrimoniaux — textes sacrés, enregistrements de
terrain, objets de collections communautaires. Deux problèmes structurels émergent :

**Problème 1 — Statistique.** Sans architecture de validation rigoureuse, les
systèmes computationnels produisent des faux positifs. La richesse combinatoire
des données culturelles rend la fausse découverte structurellement inévitable
(Witztum et al., 1994 ; McKay et al., 1999 ; Pechenick et al., 2015).

**Problème 2 — Gouvernance.** Les LLMs deviennent assez performants pour paraître
légitimes même quand ils dérivent. Sans contrôle humain architectural — pas
documentaire —, les systèmes reproduisent à l'échelle computationnelle des
pratiques d'appropriation que les cadres éthiques cherchent à prévenir.

**La réponse de ce projet** repose sur un théorème empiriquement démontré :
> *Le système le plus rigoureusement validé est, dans un sens précis, le plus
> éthiquement fiable — et le plus sobre.*

SAVEC formalise ce théorème en trois couches architecturales.
EAIFCH 2.0 l'étend vers la co-gouvernance communautaire et le contrôle de l'IA.

---

## 2. Deux fichiers, une architecture

```
savec_integration_engine_v31.py   ← FONDATION  (Layer 1 + Layer 2)
eaifch_v2.py                      ← EXTENSION  (Module 0 + Module 7)
```

`eaifch_v2.py` importe `savec_integration_engine_v31.py`.
Les deux fichiers doivent être dans le **même dossier**.

| Fichier | Rôle | Dépend de |
|---------|------|-----------|
| `savec_integration_engine_v31.py` | Valide statistiquement (Layer 1) et gouverne l'accès (Layer 2) | `numpy`, `scipy` |
| `eaifch_v2.py` | Gère la taxonomie communautaire (M0) et contrôle l'IA (M7) | `savec_integration_engine_v31.py` |

---

## 3. Installation en 2 minutes

```bash
# 1. Cloner le repository
git clone https://github.com/[votre-compte]/savec-eaifch.git
cd savec-eaifch

# 2. Installer les dépendances Python
pip install numpy scipy

# Optionnel mais recommandé pour le suivi carbone réel :
pip install codecarbon psutil

# 3. Vérifier que tout fonctionne
python savec_integration_engine_v31.py   # 8 demos Layer 1 + Layer 2
python eaifch_v2.py                      # 7 demos Module 0 + Module 7
```

Si vous voyez `All demos completed successfully.` dans les deux cas, l'installation
est correcte.

> **Python 3.9+ requis.** Testé sur Linux, macOS, Windows (WSL).

---

## 4. Démarrage rapide

### Valider un pattern statistique (Layer 1)

```python
import numpy as np
from savec_integration_engine_v31 import Layer1Validator

# Créer le validateur avec les paramètres par défaut SAVEC
validator = Layer1Validator()

# Vos données : valeurs numériques (ex. valeurs de gématria)
valeurs = np.array([7, 14, 21, 3, 8, 42, 7, 35, 11, 28])

# Valider pour le diviseur 7
result = validator.validate(
    pattern_id="mon_corpus_div7",
    observed_values=valeurs,
    divisor=7,
)

print(result.summary)
# → SAVEC Layer 1 v3.1.0 -- VALIDATED ou REJECTED
# → avec BF, CV, RVI, CO₂, H₂O...
```

### Gouverner l'accès à un objet patrimonial (Layer 2)

```python
from savec_integration_engine_v31 import (
    AccessLevel, GovernanceProtocol, resolve_layer1_to_layer2
)

# Définir le protocole de la communauté concernée
protocole = GovernanceProtocol(
    authority_id="Conseil_Wiradjuri",
    access_level=AccessLevel.COMMUNITY,
    can_export=False,
    requires_manual_audit=True,
    description="Accès réservé aux membres de la communauté.",
    epistemic_basis="community_authority",
)

# Lier Layer 1 et Layer 2
bridge = resolve_layer1_to_layer2(
    layer1_result=result,          # résultat du validate() ci-dessus
    protocols=[protocole],
    access_level=AccessLevel.COMMUNITY,
)

print(bridge.summary)
# → PASS ou BLOCKED/REJECTED
# → avec combined_confidence, epistemic_note...
```

### Appliquer des règles communautaires (Module 0)

```python
from eaifch_v2 import (
    BooleanOverrideRule, CommunityFork, TaxonomyRegistry, TaxonomyVersion,
    AccessLevel
)
from datetime import datetime, timezone, timedelta

now = datetime.now(timezone.utc)

# Règle : si objet cérémoniel ET demandeur non-membre → SACRED_SECRET
regle = BooleanOverrideRule(
    rule_id="Initiation_Override",
    description="Objet d'initiation + non-membre → restriction maximale.",
    trigger_indicators=("objet_ceremoniel", "demandeur_non_membre"),
    override_access_level=AccessLevel.SACRED_SECRET,
    signed_by="Délégué_Conseil_Wiradjuri",
    created_at=now.isoformat(),
)

# Fork communautaire
fork = CommunityFork(
    fork_id="wiradjuri_2026",
    community_id="Wiradjuri_Nation",
    base_version="1.0.0",
    signed_by="Délégué_Conseil_Wiradjuri",
    valid_from=now.isoformat(),
    valid_until=(now + timedelta(days=730)).isoformat(),
    overrides=[regle],
    weight_adjustments={"site_sacre": 35.0},
    language_additions={},
    description="Fork Wiradjuri — protocoles d'initiation.",
)
fork.sign()

# Appliquer les règles à un objet
indicateurs_actifs = ["objet_ceremoniel", "demandeur_non_membre"]
niveau_calculé = AccessLevel.RESTRICTED

niveau_final, règles_déclenchées = fork.apply_overrides(
    niveau_calculé, indicateurs_actifs
)
print(f"Niveau final : {niveau_final.name}")  # → SACRED_SECRET
print(f"Règles actives : {règles_déclenchées}")  # → ['Initiation_Override']
```

### Utiliser un LLM sous contrôle éthique (Module 7)

```python
from eaifch_v2 import AIBsandbox, MockLLMAdapter, AccessLevel

# Initialiser le sandbox avec un LLM
sandbox = AIBsandbox(MockLLMAdapter())

# Tâche autorisée
résultat = sandbox.execute_task(
    item_id="objet_001",
    task_type="preliminary_sensitivity_classification",
    prompt="Analyse ces métadonnées patrimoniales...",
    context={
        "item_sensitivity": AccessLevel.COMMUNITY.value,
        "has_community_authority": True,
        "requester_is_community_member": False,
    },
    requester_id="chercheur_001",
)
print(résultat.summary)  # → pending (validation humaine requise)

# Validation humaine obligatoire avant Layer 2
résultat.confirm(reviewer_id="délégué_communautaire")
print(résultat.can_feed_layer2)  # → True

# Tâche refusée automatiquement (CR-2)
refus = sandbox.execute_task(
    item_id="objet_sacré_001",
    task_type="theological_interpretation",  # Sur liste noire
    prompt="Interpréter ce texte sacré...",
    context={"item_sensitivity": AccessLevel.SACRED_SECRET.value},
    requester_id="chercheur_001",
)
print(refus.summary)  # → AIRefusalRecord archivé automatiquement
```

---

## 5. Structure des modules

La spécification complète définit 9 modules (M0–M8) :

```
EAIFCH 2.0 — 9 modules
│
├── M0  Governance & Taxonomy     ✅ Implémenté   eaifch_v2.py
├── M1  Sensitivity Classification ⬜ À coder     (spec disponible)
├── M2  Community Authority & CARE 🔶 Partiel     savec_v31.py + eaifch_v2.py
├── M3  Access Differentiation     🔶 Partiel     savec_v31.py
├── M4  Provenance & Consent       ⬜ À coder     (spec disponible)
├── M5  Pattern Validation         🔶 Partiel     savec_v31.py
├── M6  Sustainability & RVI       🔶 Partiel     savec_v31.py
├── M7  AI Oversight & HITL        ✅ Implémenté  eaifch_v2.py
└── M8  Impact Monitoring          ⬜ À coder     (spec disponible)

Légende : ✅ Implémenté  🔶 Partiel  ⬜ À coder
```

### SAVEC v3.1 — couches internes

```
Layer 1 — Validation statistique
  LogBayesFactor          Bayes Factor log-scale (Savage-Dickey)
  VectorisedSensitivity   Jackknife vectorisé NumPy (CV)
  HolmBonferroni          Correction step-down FWER
  RVICalculator           RVI = ΔCertainty / E_cost
  Layer1Validator   ←── point d'entrée unique Layer 1

Layer 2 — Gouvernance
  AccessLevel             Enum 5 niveaux PUBLIC→SACRED_SECRET
  GovernanceProtocol      Règle d'une autorité
  GovernanceResolver      Résolution pessimiste (max/all/any)
  ContextualRVI           Seuil RVI adapté au tier (J×base)
  EpistemicBridgeResult   Hand-off Layer1→Layer2
  resolve_layer1_to_layer2() ←── point d'entrée unique Layer 2
```

### EAIFCH 2.0 — modules

```
Module 0 — Taxonomie & Gouvernance
  TaxonomyVersion + TaxonomyRegistry   Versionnement sémantique immuable
  BooleanOverrideRule                  Règle communautaire upward-only
  CommunityFork                        Surcharge locale SHA-256
  GovernanceProtocolRecord             Cycle de vie à 5 états (sunset)
  ConflictResolver                     Cascade AUTOMATIC/MEDIATION/ESCALATION

Module 7 — Contrôle de l'IA
  ConstitutionalRule (CR-1 à CR-5)     Contraintes CARE inviolables
  LLMAdapter (abstraite)               Interface pour tout LLM
  MockLLMAdapter                       Implémentation de test
  AIBsandbox         ←── point d'entrée unique Module 7
  LLMOutputRecord                      Sortie LLM + lifecycle validation
  AIRefusalRecord                      Refus archivé (CR-5)
  SparkingSessionRecord                Session collaborative tracée
```

---

## 6. Points d'entrée principaux

> **Règle simple :** chaque couche a un seul point d'entrée.
> Tout le reste est appelé automatiquement en interne.

| Couche / Module | Point d'entrée | Produit |
|-----------------|---------------|---------|
| Layer 1 | `Layer1Validator.validate()` | `Layer1Result` |
| Layer 1 multi | `Layer1Validator.validate_multiple()` | `List[Layer1Result]` |
| Layer 2 | `resolve_layer1_to_layer2()` | `EpistemicBridgeResult` |
| M0 — taxonomie | `TaxonomyRegistry.register()` | `TaxonomyVersion` signée |
| M0 — fork | `CommunityFork.apply_overrides()` | `(AccessLevel, [règles])` |
| M0 — protocole | `create_protocol_record()` | `GovernanceProtocolRecord` |
| M0 — conflits | `ConflictResolver.resolve_conflict()` | `ConflictResolutionResult` |
| M7 — tâche | `AIBsandbox.execute_task()` | `LLMOutputRecord` ou `AIRefusalRecord` |
| M7 — sparring | `AIBsandbox.start_sparring_session()` | `SparkingSessionRecord` |

---

## 7. Flux de données complet

```
Corpus de valeurs numériques
        │
        ▼  Layer1Validator.validate()
Layer1Result  (BF, CV, RVI, epistemic_category, co2, water)
        │
        ├──► CommunityFork.apply_overrides()
        │    → AccessLevel final (peut être élevé par règle booléenne)
        │
        ▼  resolve_layer1_to_layer2()
EpistemicBridgeResult
  ├── combined_confidence  [0 … 1]
  ├── hard_block           True / False
  ├── epistemic_note       "Layer 1 validated" / "category b" / "Hard Block"
  └── contextual_rvi_eval  passes / threshold / J_multiplier
        │
        ├──► GovernanceProtocolRecord (lifecycle: ACTIVE→EXPIRED→PERMANENT)
        │
        └──► AIBsandbox.execute_task()  [si assistance LLM nécessaire]
               │
               ├── Tâche refusée → AIRefusalRecord (archivé, CR-5)
               └── Tâche autorisée → LLMOutputRecord
                       │
                       └── .confirm(reviewer) → can_feed_layer2 = True
```

**Verrou architectural unique :**
Un output `ai_generated_unvalidated` ne peut jamais atteindre Layer 2.
`LLMOutputRecord.can_feed_layer2` est `False` tant que `.confirm()` n'a pas
été appelé par un humain identifié.

---

## 8. État d'avancement

### Ce qui fonctionne maintenant (sans modification)

- ✅ Validation statistique complète : BF, CV, Holm-Bonferroni, RVI, CO₂, H₂O
- ✅ Gouvernance Layer 2 : GovernanceResolver, ContextualRVI, EpistemicBridgeResult
- ✅ Taxonomie communautaire : TaxonomyRegistry, CommunityFork, BooleanOverrideRule
- ✅ Cycle de vie des protocoles : 5 états, sunset, renouvellement, PERMANENT
- ✅ Résolution de conflits : AUTOMATIC / MEDIATION / ESCALATION
- ✅ Contrôle LLM : AIBsandbox, CR-1 à CR-5, LLMOutputValidator, Sparring

### Prochaines étapes (par priorité)

1. **Connecter le bridge Layer1→Layer2 dans Module 0**
   Appeler `resolve_layer1_to_layer2()` depuis un orchestrateur dans `eaifch_v2.py`.
   Tout est codé — c'est une connexion de 10 lignes.

2. **Coder Module 1** (SensitivityScorer)
   Classe qui prend les indicateurs actifs, applique les poids du CommunityFork,
   appelle `apply_overrides()`, retourne AccessLevel + epistemic_basis.

3. **Implémenter un vrai LLMAdapter**
   Sous-classer `LLMAdapter` pour l'API Anthropic (ou autre).
   L'interface est définie — c'est uniquement l'appel API à ajouter.

4. **Coder Module 4** (ConsentLifecycle) et **Module 8** (ImpactMonitoring)

---

## 9. Documentation

| Document | Description |
|----------|-------------|
| [`docs/Carte_coherence_SAVEC_EAIFCH.docx`](docs/) | Carte de cohérence complète : modules, flux, glossaire 22 termes |
| [`docs/EAIFCH_2_0_Specification.docx`](docs/) | Spécification architecturale des 9 modules |
| [`docs/SAVEC_JCA_manuscript_update.docx`](docs/) | Amendements manuscrit *Journal of Cultural Analytics* |

**Manuscrits académiques :**

- SAVEC — *When Rigor Protects* — soumis au *Journal of Cultural Analytics* (avril 2026)
- DSH-2025-1114 — cadre trois-phases pour l'analyse computationnelle de l'hébreu
  biblique — en révision au *Digital Scholarship in the Humanities*

---

## 10. Citation

### Citation du logiciel

```bibtex
@software{benseddik2026savec,
  author    = {Benseddik, Ahmed},
  title     = {SAVEC Integration Engine v3.1 + EAIFCH 2.0 Prototype},
  year      = {2026},
  doi       = {10.17605/OSF.IO/Y8VBU},
  url       = {https://osf.io/y8vbu},
  version   = {3.1.0 / 2.0.0},
  note      = {Statistical Architecture for Validated Ethical Curation
               × Ethical AI Framework for Cultural Heritage}
}
```

### Citation du manuscrit (preprint)

```bibtex
@unpublished{benseddik2026when,
  author = {Benseddik, Ahmed},
  title  = {When Rigor Protects: A Unified Statistical-Ethical Architecture
            for Sustainable AI in Cultural Heritage},
  year   = {2026},
  note   = {Submitted to Journal of Cultural Analytics.
            Pre-registration: DOI 10.17605/OSF.IO/Y8VBU}
}
```

---

## 11. Auteur et contact

**Ahmed Benseddik**
Chercheur indépendant
ORCID : [0009-0005-6308-8171](https://orcid.org/0009-0005-6308-8171)
OSF : [osf.io/y8vbu](https://osf.io/y8vbu)

---

### Déclaration de collaboration IA

Ce projet a été développé en collaboration humain-IA soutenue avec Claude
(Anthropic, claude-sonnet-4-6). Claude a contribué à la formalisation de
l'architecture SAVEC, à la synthèse bibliographique, à la rédaction du code et
des manuscrits, et comme partenaire critique. L'auteur humain a fourni la
conception de la recherche, toute l'expertise de domaine, la validation finale
de toutes les affirmations, et assume la responsabilité intellectuelle et éthique
complète des travaux publiés.

Cette déclaration est cohérente avec les exigences de transparence que SAVEC
impose aux systèmes computationnels : un papier argumentant pour la transparence
architecturale dans les humanités numériques serait en contradiction interne s'il
dissimulait les conditions de sa propre production.

---

*SAVEC × EAIFCH 2.0 — MIT License — Ahmed Benseddik — 2026*
