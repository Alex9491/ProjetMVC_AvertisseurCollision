from controleur.controleur import Controleur

if __name__ == "__main__":
    app = Controleur()
    try:
        app.executer()
    except KeyboardInterrupt:
        app.quitter_proprement()