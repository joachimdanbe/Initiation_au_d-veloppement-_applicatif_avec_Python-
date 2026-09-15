"""
Interface graphique Tkinter — version prête pour le déploiement.
Lancer avec : python interface_gestion.py
Nécessite la variable d'environnement GESTION_BD_MOT_DE_PASSE définie.
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from gestion_commerciale_bd import GestionCommercialeBD

class ApplicationGestion:
    def __init__(self, fenetre):
        self.gestion = GestionCommercialeBD()
        self.fenetre = fenetre
        self.fenetre.title("Gestion Clients / Commandes")
        self.fenetre.geometry("700x550")

        self._construire_formulaire()
        self._construire_recherche()
        self._construire_tableau()
        self._construire_actions()

    def _construire_formulaire(self):
        cadre = tk.LabelFrame(self.fenetre, text="Ajouter un client", padx=10, pady=10)
        cadre.pack(padx=10, pady=5, fill="x")
        tk.Label(cadre, text="Nom :").grid(row=0, column=0, sticky="e", padx=5, pady=3)
        self.champ_nom = tk.Entry(cadre, width=25)
        self.champ_nom.grid(row=0, column=1, padx=5, pady=3)
        tk.Label(cadre, text="Email :").grid(row=1, column=0, sticky="e", padx=5, pady=3)
        self.champ_email = tk.Entry(cadre, width=25)
        self.champ_email.grid(row=1, column=1, padx=5, pady=3)
        tk.Label(cadre, text="Téléphone :").grid(row=2, column=0, sticky="e", padx=5, pady=3)
        self.champ_telephone = tk.Entry(cadre, width=25)
        self.champ_telephone.grid(row=2, column=1, padx=5, pady=3)
        tk.Button(cadre, text="Ajouter", command=self.ajouter_client).grid(
            row=3, column=0, columnspan=2, pady=8)

    def _construire_recherche(self):
        cadre = tk.Frame(self.fenetre, padx=10)
        cadre.pack(fill="x")
        tk.Label(cadre, text="Rechercher :").pack(side="left")
        self.champ_recherche = tk.Entry(cadre, width=30)
        self.champ_recherche.pack(side="left", padx=5)
        self.champ_recherche.bind("<KeyRelease>", lambda event: self._rafraichir_tableau())

    def _construire_tableau(self):
        cadre = tk.LabelFrame(self.fenetre, text="Liste des clients", padx=10, pady=10)
        cadre.pack(padx=10, pady=5, fill="both", expand=True)
        colonnes = ("id", "nom", "email", "telephone", "total_depense")
        self.tableau = ttk.Treeview(cadre, columns=colonnes, show="headings")
        libelles = {"id": "ID", "nom": "Nom", "email": "Email",
                    "telephone": "Téléphone", "total_depense": "Total dépensé (€)"}
        for col in colonnes:
            self.tableau.heading(col, text=libelles[col])
            self.tableau.column(col, width=120)
        self.tableau.pack(fill="both", expand=True)

    def _construire_actions(self):
        cadre = tk.Frame(self.fenetre, pady=10)
        cadre.pack(fill="x")
        tk.Button(cadre, text="Exporter en CSV", command=self.exporter_csv).pack(side="left", padx=10)
        tk.Button(cadre, text="Supprimer le client sélectionné", command=self.supprimer_client).pack(
            side="left", padx=10)

    def ajouter_client(self):
        nom = self.champ_nom.get()
        email = self.champ_email.get()
        telephone = self.champ_telephone.get()
        try:
            self.gestion.ajouter_client(nom, email, telephone)
        except ValueError as erreur:
            messagebox.showerror("Erreur de saisie", str(erreur))
            return
        self._rafraichir_tableau()
        self.champ_nom.delete(0, tk.END)
        self.champ_email.delete(0, tk.END)
        self.champ_telephone.delete(0, tk.END)
        messagebox.showinfo("Succès", "Client ajouté avec succès.")

    def supprimer_client(self):
        selection = self.tableau.selection()
        if not selection:
            messagebox.showwarning("Attention", "Sélectionnez un client dans le tableau.")
            return
        id_client = int(self.tableau.item(selection[0])["values"][0])
        try:
            self.gestion.supprimer_client(id_client)
        except ValueError as erreur:
            messagebox.showerror("Suppression impossible", str(erreur))
            return
        self._rafraichir_tableau()

    def exporter_csv(self):
        chemin = filedialog.asksaveasfilename(defaultextension=".csv",
                                               filetypes=[("Fichier CSV", "*.csv")])
        if not chemin:
            return
        self.gestion.exporter_clients_csv(chemin)
        messagebox.showinfo("Export réussi", f"Clients exportés vers :\n{chemin}")

    def _rafraichir_tableau(self):
        for ligne in self.tableau.get_children():
            self.tableau.delete(ligne)
        terme = self.champ_recherche.get()
        for client in self.gestion.rechercher_clients(terme):
            self.tableau.insert("", tk.END, values=(
                client.id_client, client.nom, client.email,
                client.telephone, client.total_depense()
            ))


def demarrer_application():
    """Point d'entrée principal, utilisé aussi bien en dev qu'en exécutable packagé."""
    fenetre = tk.Tk()
    app = ApplicationGestion(fenetre)
    fenetre.mainloop()


if __name__ == "__main__":
    demarrer_application()
