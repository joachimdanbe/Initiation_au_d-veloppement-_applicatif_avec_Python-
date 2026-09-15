import tkinter as tk
from tkinter import messagebox
import re


def valider_email(email):
    motif = r"^[\w.\-]+@[\w\-]+\.[a-zA-Z]{2,}$"
    return re.match(motif, email) is not None


def valider_telephone(telephone):
    return telephone.isdigit() and len(telephone) == 10


def valider_formulaire():
    """Lit les champs, valide, et affiche le résultat via des boîtes de dialogue."""
    nom = champ_nom.get().strip()
    email = champ_email.get().strip()
    telephone = champ_telephone.get().strip()

    # Règle professionnelle : on ne fait JAMAIS confiance aux données saisies par l'utilisateur
    if not nom:
        messagebox.showerror("Erreur", "Le nom est obligatoire.")
        return
    if not valider_email(email):
        messagebox.showerror("Erreur", f"Email invalide : {email}")
        return
    if not valider_telephone(telephone):
        messagebox.showerror("Erreur", "Téléphone invalide (10 chiffres attendus).")
        return

    messagebox.showinfo("Succès", f"Client '{nom}' créé avec succès !")
    # Réinitialise le formulaire après succès
    champ_nom.delete(0, tk.END)
    champ_email.delete(0, tk.END)
    champ_telephone.delete(0, tk.END)


fenetre = tk.Tk()
fenetre.title("Ajouter un client")
fenetre.geometry("350x200")

# Disposition en grille : ligne, colonne
tk.Label(fenetre, text="Nom :").grid(row=0, column=0, padx=10, pady=10, sticky="e")
champ_nom = tk.Entry(fenetre, width=25)
champ_nom.grid(row=0, column=1, padx=10, pady=10)

tk.Label(fenetre, text="Email :").grid(row=1, column=0, padx=10, pady=10, sticky="e")
champ_email = tk.Entry(fenetre, width=25)
champ_email.grid(row=1, column=1, padx=10, pady=10)

tk.Label(fenetre, text="Téléphone :").grid(row=2, column=0, padx=10, pady=10, sticky="e")
champ_telephone = tk.Entry(fenetre, width=25)
champ_telephone.grid(row=2, column=1, padx=10, pady=10)

bouton_valider = tk.Button(fenetre, text="Ajouter le client", command=valider_formulaire)
bouton_valider.grid(row=3, column=0, columnspan=2, pady=15)

fenetre.mainloop()
