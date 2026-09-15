# Procédure d'installation — Application Gestion Clients/Commandes

## Prérequis
- Système Windows 10/11 (ou Linux/macOS selon la version fournie)
- Accès réseau au serveur de base de données (adresse fournie par l'administrateur)

## Étape 1 — Copier l'application
Copiez le fichier `GestionCommerciale.exe` dans un dossier de votre choix
(par exemple `C:\Applications\GestionCommerciale\`).

## Étape 2 — Configurer la connexion à la base de données
Créez un fichier `demarrer.bat` dans le même dossier, avec le contenu suivant
(remplacez les valeurs entre `<>` par celles fournies par votre administrateur) :

```bat
@echo off
set GESTION_BD_HOTE=<adresse IP du serveur>
set GESTION_BD_UTILISATEUR=<utilisateur fourni>
set GESTION_BD_MOT_DE_PASSE=<mot de passe fourni>
set GESTION_BD_NOM=gestion_commerciale
GestionCommerciale.exe
```

## Étape 3 — Lancer l'application
Double-cliquez sur `demarrer.bat`.

## En cas de problème
| Symptôme | Cause probable | Solution |
|---|---|---|
| L'application ne s'ouvre pas du tout | Antivirus bloquant l'exécutable | Ajouter une exception dans l'antivirus |
| Message "Impossible de se connecter à la base" | Mauvaise adresse IP ou mot de passe | Vérifier `demarrer.bat` avec l'administrateur |
| Message "variable d'environnement non définie" | `demarrer.bat` non utilisé (double-clic direct sur le .exe) | Toujours lancer via `demarrer.bat` |

## Contact support
En cas de problème persistant, contactez : <à compléter par le stagiaire>
