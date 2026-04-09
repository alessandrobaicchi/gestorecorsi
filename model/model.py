from database.DAO import DAO

# Nota. Il Model non sa le cose… E' un semplice passacarte! Chiede al DAO!

class Model:
    def __init__(self):
        pass

    def getCodins(self):
        return DAO.getCodins()

    def getAllCorsi(self):
        return DAO.getAllCorsi()

    def getCorsiPD(self, pd):
        return DAO.getCorsiPD(pd)

    def getCorsiPDwIscritti(self, pd):
        result = DAO.getCorsiPDwIscritti(pd)
        result.sort(key= lambda s: s[1], reverse=True)
        return result

    def getStudentiCorso(self, codins):
        studenti = DAO.getStudentiCorso(codins)
        studenti.sort(key=lambda s:s.cognome)
        return studenti

    def getCDSofCorso(self, codins):
        cds = DAO.getCDSofCorso(codins)
        cds.sort(key = lambda c: c[1], reverse=True)
        return cds
