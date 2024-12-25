import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import ttk

# Classe pour un bouton simple et arrondi
class BoutonSimple(tk.Canvas):
    def __init__(self, parent, couleur, largeur, hauteur, texte, commande):
        super().__init__(parent, width=largeur, height=hauteur, highlightthickness=0)
        self.creer_bouton_arrondi(0, 0, largeur, hauteur, 15, couleur)
        self.create_text(largeur/2, hauteur/2, text=texte, fill='white', font=("Helvetica", 12))
        self.bind("<Button-1>", lambda e: commande())
        
    def creer_bouton_arrondi(self, x1, y1, x2, y2, rayon, couleur):
        points = [x1+rayon, y1, x2-rayon, y1, x2, y1, x2, y1+rayon, x2, y2-rayon, x2, y2, x2-rayon, y2, x1+rayon, y2, x1, y2, x1, y2-rayon, x1, y1+rayon, x1, y1]
        self.create_polygon(points, smooth=True, fill=couleur)

# Classe principale de l'application
class ApplicationSnack:
    def __init__(self, root):
        self.root = root
        self.root.title("Snack Stand POS")
        self.menu = {
            "Pizza": (40.00, "pizza.jpg"),
            "Tacos": (49.00, "tacos.png"),
            "Sandwich": (30.00, "sandwich.png"),
            "Burger": (32.00, "burger.png"),
            "Frites": (15.00, "frites.png"),
            "Nuggets": (35.00, "nuggets.png"),
            "Soda": (15.00, "soda.png"),
            "Limonade": (18.00, "limonade.png")
        }
        self.panier = {}
        self.creer_fenetre_principale()
    
    def creer_fenetre_principale(self):
        tk.Label(self.root, text="Menu du Snack", font=("Helvetica", 16, "bold")).pack(pady=10)
        cadre_boutons = tk.Frame(self.root)
        cadre_boutons.pack(pady=10)
        BoutonSimple(cadre_boutons, "#4CAF50", 120, 40, "Paiement", self.paiement).pack(side=tk.LEFT, padx=5)
        BoutonSimple(cadre_boutons, "#f44336", 120, 40, "Sortie", self.root.quit).pack(side=tk.LEFT, padx=5)
        self.creer_grille_menu()
        self.root.bind('<Return>', lambda e: self.paiement())
    
    def creer_grille_menu(self):
        cadre_defilant = tk.Frame(self.root)
        cadre_defilant.pack(fill=tk.BOTH, expand=True, padx=20)
        ligne, colonne = 0, 0
        for article, (prix, chemin_img) in self.menu.items():
            cadre_article = tk.Frame(cadre_defilant, relief=tk.RAISED, borderwidth=1)
            cadre_article.grid(row=ligne, column=colonne, padx=10, pady=10, sticky="nsew")
            try:
                img = Image.open(chemin_img).resize((100, 100), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                bouton = tk.Button(cadre_article, image=photo, command=lambda i=article: self.ajouter_au_panier(i))
                bouton.image = photo
            except:
                bouton = tk.Button(cadre_article, text=article, width=15, height=5, command=lambda i=article: self.ajouter_au_panier(i))
            bouton.pack(pady=5)
            tk.Label(cadre_article, text=article, font=("Helvetica", 10, "bold")).pack()
            tk.Label(cadre_article, text=f"€{prix:.2f}").pack()
            colonne = (colonne + 1) % 4
            if colonne == 0:
                ligne += 1
    
    def ajouter_au_panier(self, article):
        fenetre_qte = tk.Toplevel(self.root)
        fenetre_qte.title(f"Ajouter {article}")
        fenetre_qte.geometry("300x200")
        tk.Label(fenetre_qte, text=f"Quantité pour {article}:", font=("Helvetica", 12)).pack(pady=10)
        var_qte = tk.StringVar(value="1")
        entree = tk.Entry(fenetre_qte, textvariable=var_qte, width=5, font=("Helvetica", 12), justify='center')
        entree.pack(pady=5)
        curseur = ttk.Scale(fenetre_qte, from_=1, to=50, orient="horizontal", command=lambda v: self.mettre_a_jour_quantite(v, var_qte, entree))
        curseur.pack(fill=tk.X, padx=20, pady=10)
        BoutonSimple(fenetre_qte, "#4CAF50", 100, 35, "Ajouter au Panier", lambda: self.confirmer_quantite(article, var_qte.get(), fenetre_qte)).pack(pady=10)
        
        def gerer_touche(event):
            try:
                actuel = int(var_qte.get())
            except:
                actuel = 1
            if event.keysym in ['Up', 'Right']:
                nouvelle_qte = min(50, actuel + 1)
            elif event.keysym in ['Down', 'Left']:
                nouvelle_qte = max(1, actuel - 1)
            elif event.keysym == 'Return':
                self.confirmer_quantite(article, var_qte.get(), fenetre_qte)
                return
            elif event.keysym == 'Escape':
                fenetre_qte.destroy()
                return
            var_qte.set(str(nouvelle_qte))
            curseur.set(nouvelle_qte)
        
        fenetre_qte.bind('<Up>', gerer_touche)
        fenetre_qte.bind('<Down>', gerer_touche)
        fenetre_qte.bind('<Left>', gerer_touche)
        fenetre_qte.bind('<Right>', gerer_touche)
        fenetre_qte.bind('<Return>', gerer_touche)
        fenetre_qte.bind('<Escape>', gerer_touche)
        entree.bind('<Return>', gerer_touche)
        entree.focus_set()
        entree.selection_range(0, tk.END)
    
    def mettre_a_jour_quantite(self, valeur, var_qte, entree):
        try:
            val = int(float(valeur))
            var_qte.set(str(val))
            entree.delete(0, tk.END)
            entree.insert(0, str(val))
        except:
            pass
    
    def confirmer_quantite(self, article, qte_str, fenetre):
        try:
            qte = int(float(qte_str))
            if 1 <= qte <= 50:
                self.panier[article] = self.panier.get(article, 0) + qte
                messagebox.showinfo("Succès", f"Ajouté {qte}x {article} au panier")
                fenetre.destroy()
            else:
                messagebox.showerror("Erreur", "Veuillez entrer un nombre entre 1 et 50")
        except:
            messagebox.showerror("Erreur", "Veuillez entrer un nombre valide")
    
    def paiement(self):
        if not self.panier:
            messagebox.showinfo("Panier Vide", "Veuillez ajouter des articles à votre panier d'abord")
            return
        total = sum(self.menu[article][0] * qte for article, qte in self.panier.items())
        reçu = "Reçu:\n\n" + "\n".join(f"{article} x{qte}: €{self.menu[article][0] * qte:.2f}" for article, qte in self.panier.items())
        reçu += f"\n\nTotal: €{total:.2f}"
        messagebox.showinfo("Paiement", reçu)
        self.panier.clear()

# Démarrer l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = ApplicationSnack(root)
    root.mainloop()