# Module 3 — Développement Applicatif — Semaine 2 (Jours 7 à 10)

Programme de stage pratique — 2e année Génie Informatique
Suite directe de la Semaine 1 (fil rouge : Gestion Clients / Commandes)

## Contenu du dossier

| Fichier | Journée | Sujet |
|---|---|---|
| `Jour7_Tests_Manuels_Structures.ipynb` | Jour 7 | Méthodologie de test, matrice de cas, cahier de recette, rapport d'anomalie, correction de bugs réels |
| `Jour8_Tests_Automatises_Pytest.ipynb` | Jour 8 | unittest, pytest, fixtures, paramétrage, mocking de la base MySQL, couverture de code |
| `Jour9_Deploiement_Application.ipynb` | Jour 9 | Variables d'environnement, packaging PyInstaller, déploiement réseau MySQL, procédure d'installation |
| `Jour10_Rapport_et_Presentation_Finale.ipynb` | Jour 10 | Structure de démonstration, gestion des imprévus, rapport technique court, auto-évaluation |

## Prérequis techniques

- Environnement de la semaine 1 (Python, Jupyter, Tkinter natif)
- `pip install pytest pytest-cov` (Jour 8)
- `pip install pyinstaller` (Jour 9)
- Pour le test réseau du Jour 9 (optionnel mais recommandé) : au moins 2 postes en réseau local avec un serveur MySQL accessible

## Point d'attention : reprise du code de la semaine 1

Chaque notebook de cette semaine **régénère** `gestion_commerciale.py` (et `gestion_commerciale_bd.py`)
via `%%writefile`, en incluant les corrections de bugs identifiées au fil des séances (notamment
la normalisation de l'email en minuscule, corrigée au Jour 7 et vérifiée par un test de
non-régression au Jour 8). Ceci permet à chaque notebook d'être autonome et exécutable
indépendamment, sans dépendre d'un état de fichiers laissé par la séance précédente.

**Recommandation pédagogique :** demandez aux étudiants de partir de LEUR PROPRE
`gestion_commerciale.py` produit en semaine 1 plutôt que celui régénéré par les notebooks
— c'est plus formateur et plus proche d'un vrai contexte de stage. Les notebooks
régénèrent le fichier uniquement pour garantir leur propre reproductibilité en démonstration.

## Point d'attention : Jour 8 (pytest) — entièrement testé

Contrairement au Jour 6 (MySQL) de la semaine 1, **tous les tests du Jour 8 s'exécutent
sans dépendance externe** : les tests sur `GestionCommerciale` utilisent uniquement la
mémoire, et les tests sur `GestionCommercialeBD` utilisent `unittest.mock` pour simuler
MySQL. Le notebook a été exécuté de bout en bout : 10 tests unittest, 16 tests pytest,
3 tests mockés, tous PASS.

## Point d'attention : Jour 9 (déploiement)

Comme au Jour 4, la génération de l'exécutable Tkinter (`pyinstaller ... interface_gestion.py`)
doit se faire **sur un poste où Tkinter est disponible** (pas garanti dans tous les
environnements serveur/sandbox). Le notebook inclut une démonstration du mécanisme
PyInstaller sur un script sans dépendance graphique, réellement testée et fonctionnelle,
pour que les étudiants comprennent le processus même avant d'avoir accès à un poste complet.

La section 4 (déploiement réseau MySQL) nécessite une coordination avec votre infrastructure
réseau de salle. Si plusieurs postes en réseau local ne sont pas disponibles, cette partie
peut être traitée de façon théorique/documentaire (rédaction de la procédure uniquement),
sans manipulation réelle — le contenu reste pédagogiquement complet.

## Recommandation de planning

Comme en semaine 1, chaque notebook est calibré pour occuper une journée complète
(environ 6h avec pauses), avec un exercice noté en fin de séance. Le Jour 10 est
volontairement plus léger en code et plus dense en travail de rédaction/préparation
individuelle — prévoir du temps de passage individuel du formateur pour écouter les
scripts de démonstration des étudiants avant la soutenance réelle.

## Cohérence avec le programme officiel du stage

Cette semaine couvre les points restants du Module 3 — Développement Applicatif
(programme officiel) :
- Tests et correction des erreurs (Jours 7 et 8)
- Introduction au déploiement d'applications (Jour 9)
- Présentation du projet réalisé (Jour 10)

Elle boucle ainsi l'intégralité des travaux pratiques prévus au programme :
conception d'une petite application de gestion (S1), création d'une base de données
(S1, Jour 6), développement des fonctionnalités principales (S1), et présentation
du projet réalisé (S2, Jour 10).

## Évaluation cumulée sur les 2 semaines

Chaque jour comporte un exercice noté avec critères explicites. À l'issue du Jour 10,
le formateur dispose de tous les éléments prévus par le barème officiel du stage pour
noter le Module 3 (30% du stage) ainsi que des éléments contribuant à la Posture
professionnelle (10%) et au Rapport et présentation finale (5%).
