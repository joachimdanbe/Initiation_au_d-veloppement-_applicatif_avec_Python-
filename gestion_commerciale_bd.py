"""Module métier connecté à MySQL — lit sa config depuis config.py (variables d'environnement)."""
import re
import mysql.connector
from mysql.connector import Error
from config import config_bd_depuis_environnement


def valider_email(email):
    motif = r"^[\w.\-]+@[\w\-]+\.[a-zA-Z]{2,}$"
    return re.match(motif, email) is not None


def valider_telephone(telephone):
    return telephone.isdigit() and len(telephone) == 10


class ClientBD:
    def __init__(self, id_client, nom, email, telephone, total_depense=0):
        self.id_client = id_client
        self.nom = nom
        self.email = email
        self.telephone = telephone
        self.total_depense_valeur = total_depense

    def total_depense(self):
        return float(self.total_depense_valeur)

    def __repr__(self):
        return f"Client(id={self.id_client}, nom='{self.nom}')"


class GestionCommercialeBD:
    """Même interface publique que GestionCommerciale, mais persistée en MySQL."""

    def __init__(self, config_bd=None):
        # Si aucune config n'est passée explicitement, on lit les variables d'environnement
        # -> C'EST CETTE LIGNE QUI RELIE L'APPLICATION AU demarrer.bat
        self.config_bd = config_bd or config_bd_depuis_environnement()

    def _connexion(self):
        try:
            return mysql.connector.connect(**self.config_bd)
        except Error as erreur:
            raise ConnectionError(f"Impossible de se connecter à MySQL : {erreur}")

    def ajouter_client(self, nom, email, telephone):
        if not nom or not nom.strip():
            raise ValueError("Le nom du client est obligatoire.")
        if not valider_email(email):
            raise ValueError(f"Email invalide : {email}")
        if not valider_telephone(telephone):
            raise ValueError(f"Téléphone invalide : {telephone}")

        connexion = self._connexion()
        try:
            curseur = connexion.cursor()
            try:
                curseur.execute(
                    "INSERT INTO clients (nom, email, telephone) VALUES (%s, %s, %s)",
                    (nom.strip(), email, telephone)
                )
                connexion.commit()
            except mysql.connector.IntegrityError:
                raise ValueError(f"Un client avec l'email {email} existe déjà.")
            return curseur.lastrowid
        finally:
            connexion.close()

    def ajouter_commande(self, id_client, date, produit, quantite, prix_unitaire):
        if quantite <= 0:
            raise ValueError("La quantité doit être strictement positive.")
        if prix_unitaire < 0:
            raise ValueError("Le prix ne peut pas être négatif.")

        connexion = self._connexion()
        try:
            curseur = connexion.cursor()
            try:
                curseur.execute(
                    """INSERT INTO commandes (id_client, date_commande, produit, quantite, prix_unitaire)
                       VALUES (%s, %s, %s, %s, %s)""",
                    (id_client, date, produit, quantite, prix_unitaire)
                )
                connexion.commit()
            except mysql.connector.IntegrityError:
                raise ValueError(f"Client inconnu (id={id_client}).")
            return curseur.lastrowid
        finally:
            connexion.close()

    def lister_clients(self):
        connexion = self._connexion()
        try:
            curseur = connexion.cursor(dictionary=True)
            curseur.execute("""
                SELECT c.id_client, c.nom, c.email, c.telephone,
                       COALESCE(SUM(cmd.quantite * cmd.prix_unitaire), 0) AS total_depense
                FROM clients c
                LEFT JOIN commandes cmd ON cmd.id_client = c.id_client
                GROUP BY c.id_client, c.nom, c.email, c.telephone
            """)
            return [ClientBD(**ligne) for ligne in curseur.fetchall()]
        finally:
            connexion.close()

    def rechercher_clients(self, terme):
        terme_sql = f"%{terme.strip()}%"
        connexion = self._connexion()
        try:
            curseur = connexion.cursor(dictionary=True)
            curseur.execute("""
                SELECT c.id_client, c.nom, c.email, c.telephone,
                       COALESCE(SUM(cmd.quantite * cmd.prix_unitaire), 0) AS total_depense
                FROM clients c
                LEFT JOIN commandes cmd ON cmd.id_client = c.id_client
                WHERE c.nom LIKE %s OR c.email LIKE %s
                GROUP BY c.id_client, c.nom, c.email, c.telephone
            """, (terme_sql, terme_sql))
            return [ClientBD(**ligne) for ligne in curseur.fetchall()]
        finally:
            connexion.close()

    def supprimer_client(self, id_client):
        connexion = self._connexion()
        try:
            curseur = connexion.cursor()
            curseur.execute("SELECT COUNT(*) FROM commandes WHERE id_client = %s", (id_client,))
            if curseur.fetchone()[0] > 0:
                raise ValueError("Impossible de supprimer ce client : des commandes lui sont associées.")
            curseur.execute("DELETE FROM clients WHERE id_client = %s", (id_client,))
            connexion.commit()
            if curseur.rowcount == 0:
                raise ValueError(f"Client inconnu (id={id_client}).")
        finally:
            connexion.close()

    def exporter_clients_csv(self, chemin_fichier):
        import csv
        with open(chemin_fichier, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Nom", "Email", "Téléphone", "Total dépensé (€)"])
            for client in self.lister_clients():
                writer.writerow([client.id_client, client.nom, client.email,
                                  client.telephone, client.total_depense()])