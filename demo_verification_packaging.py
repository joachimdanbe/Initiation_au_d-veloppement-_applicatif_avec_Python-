"""Petit script de démonstration pour vérifier concrètement le mécanisme PyInstaller."""
from gestion_commerciale import GestionCommerciale

gestion = GestionCommerciale()
client = gestion.ajouter_client("Démo Packaging", "demo@test.com", "0611223344")
print(f"Application empaquetée fonctionnelle : client créé -> {client}")
print("Si ce message s'affiche depuis l'exécutable dist/, le packaging a réussi.")
