from database.DAO import DAO

# Nota. Il Model non sa le cose… E' un semplice passacarte! Chiede al DAO!
#       Il Model è l'unico che parla col Controller e con il DAO.

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
        result = DAO.getCorsiPDwIscritti(pd)    # result è una lista
        result.sort(key= lambda s: s[1], reverse=True)
        # Capiterà spesso di dover ordinare le liste di tuple.
        # Non è richiesto dall'esercizio ma decido di ordinare questa lista di tuple per numero di iscritti a corsi,
        # in senso decrescente. Posso fare ciò nel DAO, nel Model e nel Controller, però è più corretto farlo nel Model,
        # perché il Model è quello che manipola i dati.
        # Per dire come ordinare la lista conviene usare una lambda function.
        # La chiave per ordinare sarà una lambda function: key = lamda s: s[1]
        # Ho messo s[1], perché? Perché s è un elemento della lista. La lista contiene tuple, quindi, s è una tupla.
        # Il primo elemento di questa tupla s (s[0]) è il corso, mentre il secondo elemento (s[1]) è il numero di iscritti.
        return result

    def getStudentiCorso(self, codins):
        studenti = DAO.getStudentiCorso(codins)     # studenti è una lista
        studenti.sort(key=lambda s:s.cognome)
        # s è un elemento della lista studenti ed è un oggetto di tipo studente, quindi, accedo al campo cognome.
        return studenti

    def getCDSofCorso(self, codins):
        cds = DAO.getCDSofCorso(codins)
        cds.sort(key = lambda c: c[1], reverse=True)
        return cds
