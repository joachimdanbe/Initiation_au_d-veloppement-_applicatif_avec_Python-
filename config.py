"""
Configuration de l'application, lue depuis les variables d'environnement.
Ce fichier peut être partagé/versionné sans risque : il ne contient AUCUN secret.
"""
import os


def config_bd_depuis_environnement():
    """
    Construit la configuration de connexion à la base de données à partir
    des variables d'environnement définies par demarrer.bat.
    """
    return {
        "host": os.environ.get("GESTION_BD_HOTE", "localhost"),
        "user": os.environ.get("GESTION_BD_UTILISATEUR", "root"),
        "password": os.environ.get("GESTION_BD_MOT_DE_PASSE", ""),
        "database": os.environ.get("GESTION_BD_NOM", "gestion_commerciale"),
    }


def verifier_configuration():
    """Vérifie que le mot de passe a bien été fourni (pas la valeur par défaut vide)."""
    config = config_bd_depuis_environnement()
    if not config["password"]:
        raise EnvironmentError(
            "La variable d'environnement GESTION_BD_MOT_DE_PASSE n'est pas définie.\n"
            "Lancez l'application via demarrer.bat, pas en double-cliquant directement sur le .exe."
        )
    return config
