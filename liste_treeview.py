import tkinter as tk
from tkinter import ttk

# Données de démonstration (viendront de GestionCommerciale demain)
clients_demo = [
    (1, "Amina Traoré", "amina@example.com", "0612345678"),
    (2, "Jean Kouassi", "jean.k@example.com", "0623456789"),
]

fenetre = tk.Tk()
fenetre.title("Liste des clients")
fenetre.geometry("500x200")

colonnes = ("id", "nom", "email", "telephone")
tableau = ttk.Treeview(fenetre, columns=colonnes, show="headings")

# En-têtes de colonnes
tableau.heading("id", text="ID")
tableau.heading("nom", text="Nom")
tableau.heading("email", text="Email")
tableau.heading("telephone", text="Téléphone")

tableau.column("id", width=40)
tableau.column("nom", width=150)
tableau.column("email", width=180)
tableau.column("telephone", width=100)

# Remplissage avec les données
for client in clients_demo:
    tableau.insert("", tk.END, values=client)

tableau.pack(padx=10, pady=10, fill="both", expand=True)

fenetre.mainloop()
