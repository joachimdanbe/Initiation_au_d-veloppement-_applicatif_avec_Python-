import tkinter as tk

# 1. Créer la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Gestion Commerciale - Test")
fenetre.geometry("400x200")  # largeur x hauteur en pixels

# 2. Créer un widget (une étiquette de texte)
etiquette = tk.Label(fenetre, text="Bienvenue dans l'application de gestion commerciale", wraplength=350)
etiquette.pack(pady=20)  # pady = espace vertical autour du widget

# 3. Créer un bouton avec une action
def dire_bonjour():
    etiquette.config(text="Bonjour, stagiaire !")

bouton = tk.Button(fenetre, text="Cliquez-moi", command=dire_bonjour)
bouton.pack(pady=10)

4. Lancer la boucle principale (garde la fenêtre ouverte)
fenetre.mainloop()
