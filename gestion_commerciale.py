"""
Module métier complet : logique de gestion des clients et commandes.
Version finale de la semaine 1 (recherche, modification, suppression, export).
"""
import re
import csv


def valider_email(email):
    motif = r"^[\w.\-]+@[\w\-]+\.[a-zA-Z]{2,}$"
    return re.match(motif, email) is not None


def valider_telephone(telephone):
    return telephone.isdigit() and len(telephone) == 10


class Client:
    def __init__(self, id_client, nom, email, telephone):
        if not nom or not nom.strip():
            raise ValueError("Le nom du client est obligatoire.")
        if not valider_email(email):
            raise ValueError(f"Email invalide : {email}")
        if not valider_telephone(telephone):
            raise ValueError(f"Téléphone invalide : {telephone}")
        self.id_client = id_client
        self.nom = nom.strip()
        self.email = email
        self.telephone = telephone
        self.commandes = []

    def ajouter_commande(self, commande):
        self.commandes.append(commande)

    def total_depense(self):
        return round(sum(c.total() for c in self.commandes), 2)

    def __repr__(self):
        return f"Client(id={self.id_client}, nom='{self.nom}')"


class Commande:
    def __init__(self, id_commande, client, date, produit, quantite, prix_unitaire):
        if quantite <= 0:
            raise ValueError("La quantité doit être strictement positive.")
        if prix_unitaire < 0:
            raise ValueError("Le prix ne peut pas être négatif.")
        self.id_commande = id_commande
        self.client = client
        self.date = date
        self.produit = produit
        self.quantite = quantite
        self.prix_unitaire = prix_unitaire

    def total(self):
        return round(self.quantite * self.prix_unitaire, 2)

    def __repr__(self):
        return f"Commande(id={self.id_commande}, produit='{self.produit}')"


class GestionCommerciale:
    def __init__(self):
        self._clients = {}
        self._prochain_id_client = 1
        self._prochain_id_commande = 1

    def ajouter_client(self, nom, email, telephone):
        for client in self._clients.values():
            if client.email == email:
                raise ValueError(f"Un client avec l'email {email} existe déjà.")
        client = Client(self._prochain_id_client, nom, email, telephone)
        self._clients[client.id_client] = client
        self._prochain_id_client += 1
        return client

    def ajouter_commande(self, id_client, date, produit, quantite, prix_unitaire):
        if id_client not in self._clients:
            raise ValueError(f"Client inconnu (id={id_client}).")
        client = self._clients[id_client]
        commande = Commande(self._prochain_id_commande, client, date, produit, quantite, prix_unitaire)
        client.ajouter_commande(commande)
        self._prochain_id_commande += 1
        return commande

    def lister_clients(self):
        return list(self._clients.values())

    def obtenir_client(self, id_client):
        return self._clients.get(id_client)

    def rechercher_clients(self, terme):
        terme = terme.lower().strip()
        if not terme:
            return self.lister_clients()
        return [
            c for c in self._clients.values()
            if terme in c.nom.lower() or terme in c.email.lower()
        ]

    def clients_sans_commande(self):
        return [c for c in self._clients.values() if not c.commandes]

    def clients_par_depense_decroissante(self):
        return sorted(self._clients.values(), key=lambda c: c.total_depense(), reverse=True)

    def meilleur_client(self):
        if not self._clients:
            return None
        return max(self._clients.values(), key=lambda c: c.total_depense())

    def modifier_client(self, id_client, nom=None, email=None, telephone=None):
        client = self._clients.get(id_client)
        if client is None:
            raise ValueError(f"Client inconnu (id={id_client}).")

        if email is not None and email != client.email:
            if not valider_email(email):
                raise ValueError(f"Email invalide : {email}")
            for autre in self._clients.values():
                if autre.id_client != id_client and autre.email == email:
                    raise ValueError(f"Un autre client utilise déjà l'email {email}.")
            client.email = email

        if telephone is not None:
            if not valider_telephone(telephone):
                raise ValueError(f"Téléphone invalide : {telephone}")
            client.telephone = telephone

        if nom is not None:
            if not nom.strip():
                raise ValueError("Le nom ne peut pas être vide.")
            client.nom = nom.strip()

        return client

    def supprimer_client(self, id_client):
        client = self._clients.get(id_client)
        if client is None:
            raise ValueError(f"Client inconnu (id={id_client}).")
        if client.commandes:
            raise ValueError(
                f"Impossible de supprimer '{client.nom}' : il a {len(client.commandes)} "
                "commande(s) enregistrée(s). Envisagez de l'archiver plutôt."
            )
        del self._clients[id_client]

    def exporter_clients_csv(self, chemin_fichier):
        with open(chemin_fichier, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Nom", "Email", "Téléphone", "Total dépensé (€)"])
            for client in self.lister_clients():
                writer.writerow([client.id_client, client.nom, client.email,
                                  client.telephone, client.total_depense()])
