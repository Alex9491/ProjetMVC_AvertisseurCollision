from modele.platine import Platine
from vue.vue import Vue
import tkinter as tk


class Controleur:
    # Méthode qui permet d'initialiser
    def __init__(self):
        self.root = tk.Tk()

        self.vue = Vue(self.root)
        self.vue.set_controleur(self)

        self.platine = Platine(self)

    # Méthode qui permet d'éxécuter l'application
    def executer(self):
        self.platine.initialiser()
        self.root.mainloop()

    # Méthode qui permet de faire la logique du bouton vert
    def bouton_vert_appuye(self):
        if self.platine.systeme_actif:
            self.platine.arreter_systeme()
        else:
            self.platine.demarrer_systeme()

    # Méthode qui permet de prendre la mesure si on appuye sur le bouton rouge
    def bouton_rouge_appuye(self):
        self.platine.prendre_mesure()

    # Méthode qui affiche le nb détection
    def nouvelle_detection(self, nb):
        self.vue.afficher_detection(nb)

    # Méthode qui permet de configurer le nb de collision dans l'interface graphique
    def configurer_collision(self):
        # Exception pour gérer l'erreur si l'utilisateur tape un lettre (ex. abc-->Valeur invalide)
        try:
            nb = int(self.vue.entree_collision.get())

            if nb <= 0:
                return

            self.platine.definir_collision(nb)
        except ValueError:
            print("Valeur invalide")
    # Méthode qui permet de sauvegarder les mesures dans le BD
    def sauvegarder_bd(self):
        for mesure in self.platine.liste_mesures:
            self.platine.gestionnaireBD.ajouterMesure(mesure.donneeMesure)
            print("Sauvegarder:", mesure.donneeMesure)
        self.platine.liste_mesures.clear()
        self.vue.listbox_mesures.delete(0, tk.END)
    
    # Méthode qui permet de quitter proprement l'application
    def quitter_proprement(self):

        print("Fermeture propre de l'application...")
        self.platine.enExecution = False
        self.platine.systeme_actif = False
        self.platine.led_verte.off()
        self.platine.led_rouge.off()
        self.platine.buzzer.off()
        self.platine.graphique.value = 0
        self.platine.ecran.clear()
        self.platine.gestionnaireBD.fermetureDB()

        print("Application fermée proprement")
