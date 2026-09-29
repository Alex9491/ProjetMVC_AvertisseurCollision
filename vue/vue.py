import tkinter as tk
import moduleCapteurs.LCD as mLCD


class Vue:
    # Méthode qui permet d'initialiser
    def __init__(self, fenetre):
        self.fenetre = fenetre
        self.controleur = None
        
        # Configuration de la fenetre
        self.fenetre.title("Tp Synthese")
        self.fenetre.geometry("600x500")
        
        # Étiquette du nb détections collisions
        self.lbl_collision = tk.Label(self.fenetre,text="Nombre de detections collision")
        self.lbl_collision.pack()

        # Champ qu'on peut saisir nb de collisions
        self.entree_collision = tk.Entry(self.fenetre)
        self.entree_collision.pack()

        # Bouton collision
        self.btn_collision = tk.Button(self.fenetre,text="Configurer collision",command=self.configurer_collision)
        self.btn_collision.pack()

        self.ecran = mLCD.LCD(0x27, 2)
        
        self.lbl_etat = tk.Label(self.fenetre,text="Systeme desactive",bg="red",fg="white",width=20)

        self.lbl_etat.pack()
        
        # Listbox
        self.listbox_mesures = tk.Listbox(self.fenetre,width=60,height=10)
        self.listbox_mesures.pack()
        
        # Barre de défilement permettant de naviguer dans les mesures de la listbox
        self.scrollbar = tk.Scrollbar(self.fenetre)
        self.scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
        self.listbox_mesures.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox_mesures.yview)
        
        self.btn_sauvegarder = tk.Button(self.fenetre,text="Sauvegarder BD",command=self.sauvegarder_bd)
        self.btn_sauvegarder.pack()

    # Méthode qui définit le controleur principal
    def set_controleur(self, controleur):
        self.controleur = controleur

    # Méthode qui permet d'afficher les détections dans l'écran LCD
    def afficher_detection(self, nb):

        self.ecran.clear()

        self.ecran.message_at(
            "Detections:",
            1,
            0
        )

        self.ecran.message_at(
            f"{nb}",
            2,
            0
        )

    # Méthode qui permet de clear l'écran LCD
    def clear(self):
        self.ecran.clear()
    
    # Méthode qui permet de configurer collision
    def configurer_collision(self):

        if self.controleur:
            self.controleur.configurer_collision()
    
    # Méthode qui permet de changer l'état dans l'interface graphique si active = vert , désactive = rouge
    def changer_etat(self, actif):

        if actif:

            self.lbl_etat.config(
            text="Systeme active",
            bg="green"
            )

        else:

            self.lbl_etat.config(
            text="Systeme desactive",
            bg="red"
            )
    
    # Méthode qui permet d'ajouter mesure dans listbox
    def ajouter_mesure(self, mesure):

        self.listbox_mesures.insert(
            tk.END,
            mesure
        )
    
    # Méthode qui appelle sauvegarder bd dans controleur
    def sauvegarder_bd(self):
        if self.controleur:
            self.controleur.sauvegarder_bd()