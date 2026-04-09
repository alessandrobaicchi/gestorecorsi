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
        cursor = cnx.cursor(dictionary=True)

        query = """SELECT *
                    FROM corso c
                    WHERE c.pd = %s"""

        cursor.execute(query, (pd,))

        res = []
        for row in cursor:
            res.append(Corso(**row))

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
            res.append(Studente(**row))

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
