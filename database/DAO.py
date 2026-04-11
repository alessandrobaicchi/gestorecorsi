from database.DB_connect import DBConnect
from model.corso import Corso
from model.studente import Studente


# Nota. I metodi del DAO() hanno la stessa struttura ed infatti viene data dal Professore. Ciò che cambia,
#       e devo scrivere io, è la query e cosa fare con i dati presi dal DB.


class DAO():

    @staticmethod
    def getCodins():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        # Le query le scrivo in DBeaver perché lì posso testarle. Poi se vanno bene le incollo qui in Python
        query = """select codins FROM corso"""

        cursor.execute(query)

        res = []
        # Metto i dati presi dal DB in una lista (res)
        for row in cursor:
            res.append(row["codins"])
        # codins è il nome della colonna della tabella del DB
        # Non sto creando un DTO perché qui non mi serve: sto gestendo solo stringhe.

        cursor.close()
        cnx.close()
        return res
        # Questo metodo getCodins() restituisce una lista di stringhe con tutti gli insegnamenti.



    @staticmethod
    def getAllCorsi():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """select * FROM corso"""

        cursor.execute(query)

        res = []
        # Qui appendo in res non più una stringa (come in getCodins()), ma un nuovo oggetto Corso.
        for row in cursor:
            res.append(Corso(
                codins = row["codins"],
                crediti = row["crediti"],
                nome = row["nome"],
                pd = row["pd"]
            ))
        # Sto creando una lista di oggetti di tipo Corso. Questa lista viene passata al Model
        # (che la chiama con il metodo DAO.getAllCorsi()).


        cursor.close()
        cnx.close()
        return res



    @staticmethod
    def getCorsiPD(pd):
        cnx = DBConnect.get_connection()
        # Creo un oggetto cursore che uso per fare (eseguire) le query e mi restituisce dizionari.
        # Oltre a ciò il cursore riceve le righe dal DB e me ne dà una alla volta nel ciclo for che segue
        cursor = cnx.cursor(dictionary=True)
        # dictionary=TRUE significa che ogni riga dal DB verrà rappresentata come un dizionario in Python,
        # ovvero una cosa del genere:
        # {
        #     "codins": 101,
        #     "nome": "Analisi 1",
        #     "pd": 1
        # }
        # Ciò è fondamentale perché dopo posso fare l'unpacking del dizionario nei parametri del costruttore

        query = """ SELECT *
                    FROM corso c
                    WHERE c.pd = %s"""

        cursor.execute(query, (pd,))
        # Esegue la query. Per eseguire la query il cursore devo passargli una tupla di parametri

        res = []
        # Con questo ciclo for scorro le righe della tabella corso
        for row in cursor:
            res.append(Corso(**row))    # UNPACKING del dizionario nei parametri del costruttore
            # Con questa riga di codice salvo in res le varie righe (row)

        # Nota. In getAllCorsi() esplicito tutti i paremetri del oggetto Corso.
        #       Però, se ho l'accortezza di dare ai nomi degli attributi dell'oggetto DTO (qui Corso)
        #       lo stesso nome delle rispettive colonne nel database,
        #       allora posso fare direttamente l'unpackong della riga, e qui ho fatto così.
        #       Questo semplifica la scrittura del costruttore.

        cursor.close()
        cnx.close()
        return res



    @staticmethod
    def getCorsiPDwIscritti(pd):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """SELECT c.codins, c.crediti, c.nome, c.pd, count(*) as n
                    FROM corso c, iscrizione i 
                    WHERE c.codins = i.codins 
                    and c.pd = %s
                    group by c.codins, c.crediti, c.nome, c.pd"""

        cursor.execute(query, (pd,))

        res = []
        for row in cursor:
            res.append( (Corso(codins = row["codins"],
                                crediti = row["crediti"],
                                nome = row["nome"],
                                pd = row["pd"]),
                         row["n"] ))
        # Questa volta il risultato è una tupla Corso e numero di iscritti n a quel Corso.
        # Dove n lo prendo come row di n e i parametri di Corso li leggo in maniera esplicita.
        cursor.close()
        cnx.close()
        return res



    @staticmethod
    def getStudentiCorso(codins):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """SELECT s.*
                    FROM studente s, iscrizione i 
                    WHERE s.matricola = i.matricola 
                    and i.codins = %s"""

        cursor.execute(query, (codins,))

        res = []
        for row in cursor:
            res.append(Studente(**row))     # UNPACKING del dizionario nei parametri del costruttore
            # Qui uso il DTO Studente
        cursor.close()
        cnx.close()
        return res



    @staticmethod
    def getCDSofCorso(codins):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """SELECT s.CDS, count(*) as n
                    FROM studente s, iscrizione i 
                    WHERE s.matricola = i.matricola 
                    and i.codins = %s
                    and s.CDS != ""
                    group by s.CDS """

        cursor.execute(query, (codins,))

        res = []
        for row in cursor:
            res.append((row["CDS"], row["n"]))

        cursor.close()
        cnx.close()
        return res
