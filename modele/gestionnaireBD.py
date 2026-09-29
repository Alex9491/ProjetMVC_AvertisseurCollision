import sqlite3, datetime, json, os


class GestionnaireBD:
    # Méthode qui permet initialiser
    def __init__(self, nomBD="donneesBD.db"):
        #Création du chemin du dossier fichiersBD
        dossier = os.path.join(
            os.path.dirname(__file__),
            "..",
            "fichiersBD"
        )
        # Création du dossier s'il n'existe pas
        if not os.path.exists(dossier):
            os.makedirs(dossier)
        self.cheminBD = os.path.join(
            dossier,
            nomBD
        )
        # Les attributs
        self.connexion = None
        self.table_mesure = "MESURES"
        self.cle_no = "ID"
        self.cle_date = "DATE_HEURE"
        self.cle_donnee = "DONNEE"
        self.creationTable()

    ##### connexion BD
    # Méthode qui permet d'ouvrir la connexion SQLite
    def connexionBD(self):
        try:
            self.connexion = sqlite3.connect(
                self.cheminBD
            )
            print("Ouverture BD")
        except sqlite3.Error as error:
            print(
                "Erreur connexion BD",
                error
            )
    ##### fermeture BD
    # Méthode qui permet de fermer la connexion SQLite
    def fermetureDB(self):
        if self.connexion:
            self.connexion.close()
            print("Fermeture BD")

    ##### ajouter mesure
    # Méthode qui permet d'ajouter une mesure dans la table Mesure
    def ajouterMesure(self, donneeMesure):

        sql_insert = (
            "INSERT INTO "
            + self.table_mesure
            + " ("
            + self.cle_date
            + ", "
            + self.cle_donnee
            + ") VALUES (?, ?);"
        )

        # Ouverture de la connexion
        self.connexionBD()

        try:
            # Création curseur
            cur_insert = self.connexion.cursor()

            # Création date actuelle
            dateMesure = (
                datetime.datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )
            # Transforme dictionnaire en Json
            donnee_json = json.dumps(
                donneeMesure
            )
            donnees_param = (
                dateMesure,
                donnee_json
            )
            # Éxécution de la requete SQL
            cur_insert.execute(
                sql_insert,
                donnees_param
            )
            # Sauvegarde les changements
            self.connexion.commit()

            print(
                "Mesure sauvegardee"
            )
            # Ferme curseur
            cur_insert.close()

        except sqlite3.Error as error:

            print(
                "Erreur ajout mesure",
                error
            )
        finally:

            self.fermetureDB()
    ##### verifier table
    # Méthode qui permet de vérifier l'existance de la table
    def verifierExisteTable(self, table):

        existe = False
        # Création curseur
        cur = self.connexion.cursor()

        # Requete SQL
        sql_tableExiste = (
            "SELECT count(name) "
            "FROM sqlite_master "
            "WHERE type='table' "
            "AND name='"
            + table
            + "'"
        )

        try:

            cur.execute(sql_tableExiste)

            if cur.fetchone()[0] == 1:

                existe = True

        except sqlite3.Error as error:

            print(
                "Erreur verification table",
                error
            )

        return existe
    ##### creation table
    # Méthode qui permet de créer table
    def creationTable(self):
        tableMesure = (
            "CREATE TABLE "
            + self.table_mesure
            + " ("
            + self.cle_no
            + " INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "
            + self.cle_date
            + " TEXT NOT NULL, "
            + self.cle_donnee
            + " TEXT NOT NULL);"
        )

        # Ouverture connexion
        self.connexionBD()

        # Vérification si la table existe déja
        if self.verifierExisteTable(
            self.table_mesure
        ):

            print("Table existe deja")

        else:
            try:
                self.connexion.execute(
                    tableMesure
                )
                print("Creation table")
            except sqlite3.Error as error:
                print(
                    "Erreur creation table",
                    error
                )
        self.fermetureDB()