from gpiozero import Button, LED, MotionSensor, Buzzer, LEDBarGraph
import moduleCapteurs.LCD as mLCD
import threading
from modele.mesure import Mesure
from time import sleep
from modele.gestionnaireBD import GestionnaireBD


class Platine:
    # Méthode qui permet d'initialiser les composantes
    def __init__(self, controleur):

        self.controleur = controleur

        self.bouton_rouge = Button(13)
        self.bouton_vert = Button(19)

        self.led_verte = LED(12)
        self.led_rouge = LED(21)
        
        self.buzzer = Buzzer(16)
        
        self.gestionnaireBD = GestionnaireBD()
        self.liste_mesures = []
        
        self.graphique = LEDBarGraph(
        23, 24, 5, 6, 20,
        26, 4, 17, 27, 22,
        pwm=True
        )
        self.graphique.value = 0
        
        self.collision_active = False

        self.capteur = MotionSensor(25)
        self.nb_collision = 5
        self.compteurDetection = 0
        

        self.ecran = mLCD.LCD(0x27, 2)

        self.systeme_actif = False
        self.enExecution = False
        
        # Permet lier les événements boutons
        self._lier_evenements()

    # Méthode qui permet lier
    def _lier_evenements(self):

        self.bouton_vert.when_pressed = self.controleur.bouton_vert_appuye
        self.bouton_rouge.when_pressed = self.controleur.bouton_rouge_appuye

    # Méthode qui permet d'initialiser l'état du systeme
    def initialiser(self):

        self.systeme_actif = False
        self.enExecution = False

        self.led_rouge.on()
        self.led_verte.off()
        self.graphique.value = 0

        self.ecran.clear()
    
    # Méthode qui permet définir collision
    def definir_collision(self, nb):

        self.nb_collision = nb

        self.ecran.clear()
        self.ecran.message_at("Collision:", 1, 0)
        self.ecran.message_at(f"{nb} detections", 2, 0)

    # Méthode qui démarre systeme
    def demarrer_systeme(self):
        self.systeme_actif = True
        self.enExecution = True
        self.compteurDetection = 0
        self.led_rouge.off()
        self.led_verte.on()
        self.collision_active = False
        
        self.ecran.clear()
        self.ecran.message_at("Systeme", 1 ,0)
        self.ecran.message_at("active", 2, 0)
        self.controleur.vue.changer_etat(True)
        sleep(2)

        threading.Thread(target=self._loop_capteur, daemon=True).start() #permet d'activer thread
    # Méthode qui permet de loop capteur et logique de l'application
    def _loop_capteur(self):

        while self.enExecution and not self.collision_active:
            #lecture du capteur PIR
            mouvement = self.capteur.motion_detected

            print("Mouvement:", mouvement)

            if mouvement:
                
                # Incrémente compteur
                self.compteurDetection += 1
                
                # Permet de calculer niveau du tableau LED
                niveau = self.compteurDetection / self.nb_collision

                # Limite maximum
                if niveau > 1:
                    niveau = 1

                # Mise a jour LEDS
                self.graphique.value = niveau

                print("Compteur:", self.compteurDetection)

                self.controleur.nouvelle_detection(
                    self.compteurDetection
                )

        #MODE 1 (Aucune alerte)
            if self.compteurDetection < self.nb_collision - 10:

                self.buzzer.off()

        #MODE 2 (Alerte)
            elif self.compteurDetection < self.nb_collision:

                self.buzzer.on()
                sleep(0.1)
                self.buzzer.off()
                sleep(0.3)

        #MODE 3 (COLLISION)
            else:
                # Vérification pour éviter d'éxécuter plusieurs fois les actions de collision
                if not self.collision_active:

                    self.collision_active = True

                    self.ecran.clear()
                    self.ecran.message_at("COLLISION", 1, 0) #Affichage sur écran LCD (collision)
                    self.led_verte.off() #led verte off
                    self.clignoter_led(self.led_rouge) # permet de clignoter led
                    self.clignoter_buzzer() # permet de clignoter buzzer
                    self.graphique.value = 1

                sleep(0.2)

    # Méthode qui arrete systeme
    def arreter_systeme(self):

        self.systeme_actif = False
        self.enExecution = False

        self.led_verte.off()
        self.led_rouge.on()
        
        self.buzzer.off()
        
        # Affichage sur l'écran LCD
        self.ecran.message_at(
        "Systeme",
        1,
        0
        )

        self.ecran.message_at(
        "desactive",
        2,
        0
        )

        self.controleur.vue.changer_etat(False)
    
    # Méthode qui permet de clignoter led 3x fois
    def clignoter_led(self, led):

        compteur = 0

        while compteur < 3:

            led.on()
            sleep(0.2)

            led.off()
            sleep(0.2)

            compteur += 1

        led.on()
    
    # Méthode qui permet de prendre mesure
    def prendre_mesure(self):

        if self.compteurDetection >= self.nb_collision:
            return

        self.ecran.clear()
        self.ecran.message_at("Prise mesure", 1, 0)
        self.ecran.message_at(f"{self.compteurDetection} detect", 2, 0)
        self.clignoter_led(self.led_verte)

        donnees = {
        "collision": self.nb_collision,
        "detection": self.compteurDetection,
        "leds": round(self.graphique.value * 10)
       
    }
        print("Mesure ajoutée :", donnees)
        mesure = Mesure(donnees)

        self.liste_mesures.append(mesure)

        self.controleur.vue.ajouter_mesure(mesure)
    
    # Méthode qui permet de clignoter buzzer
    def clignoter_buzzer(self, nb=3):

        for _ in range(nb):

            print("Buzzer on")
            self.buzzer.on()
            sleep(0.2)

            print("Buzzer off")
            self.buzzer.off()
            sleep(0.2)