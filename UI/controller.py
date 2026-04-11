import flet as ft

from model.model import Model


class Controller:
    def __init__(self, view):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = Model()
        self._ddCodinsValue = None



    def handlePrintCorsiPD(self, e):
        # Questo metodo ha come argomento l'evento "e".
        # L'evento "e" è generato dalla pressione del rispetto pulsante (del View) fatta dall'utente.

        # Questo metodo deve recuperare dall'interfaccia grafica qual è il periodo didattico scelto dall'utente,
        # poi fare la query al database tramite il Model e poi stampare i dati.

        self._view.txt_result.controls.clear()

        # Per prima cosa recupero il periodo didattico scelto dall'utente tramite il corrispettivo Dropdown.
        # Però, questo periodo didattico sarà la stringa I o II, ma nella query devo passare un valore intero 1 o 2.
        # Dunque, verifico il valore di pd (in stringhe) e lo converto in interi.
        pd = self._view.ddPD.value

        # Può succedere che pd sia None, ovvero l'utente non ha fatto nessuna scelta nel Dropdown.
        # In tal caso lo dico all'utente. Lo si può fare con un messaggio, ma dato che ho creato
        # un metodo create_alert() nel View uso tale metodo (per il Prof non è l'approccio da usare,
        # perché vado ad aggiungere complessità).
        if pd is None:
            (self._view.create_alert
             ("Attenzione, selezionare un periodo didattico."))
            self._view.update_page()    # Aggiorno la pagina
            return

        if pd == "I":
            pdInt = 1
        else: pdInt = 2

        # A questo punto ho tutto per poter fare la query.

        corsiPD = self._model.getCorsiPD(pdInt)
        # getCorsiPD() è un metodo del Model (che accetta il parametro pdInt) che va a chiedere al DAO
        # di fare la query (dal punto di vista del Controller questa cosa non è importante).

        # corsiPD è una lista.
        # Può succedere che questa lista sia vuota, ad esempio se la mia query non ha ottenuto risultati.

        if not len(corsiPD):
            self._view.txt_result.controls.append(ft.Text(f"Nessun corso trovato per il {pd} periodo didattico."))
            self._view.update_page()
            return

        # Altrimenti vuol dire che corsiPD conterrà una lista di corsi. Così ciclo su questa lista di corsi e la stampo.
        # La stampa sfrutta il metodo __str__ dell'oggetto Corso, che ho scritto appositamente.
        self._view.txt_result.controls.append(
            ft.Text(f"Di seguito i corsi del {pd} periodo didattico:"))
        for c in corsiPD:
            self._view.txt_result.controls.append(ft.Text(c))
        self._view.update_page()



    def handlePrintIscrittiCorsiPD(self, e):
        self._view.txt_result.controls.clear()

        pd = self._view.ddPD.value

        if pd is None:
            (self._view.create_alert
             ("Attenzione, selezionare un periodo didattico."))
            self._view.update_page()
            return

        if pd == "I":
            pdInt = 1
        else:
            pdInt = 2

        corsi = self._model.getCorsiPDwIscritti(pdInt)

        if not len(corsi):
            self._view.txt_result.controls.append(
                ft.Text(f"Nessun corso trovato per il {pd} periodo didattico."))
            self._view.update_page()
            return

        self._view.txt_result.controls.append(
            ft.Text(f"Di seguito i corsi del {pd} periodo didattico con dettaglio iscritti:"))
        for c in corsi:
            self._view.txt_result.controls.append(
                ft.Text(f"{c[0]} -- N Iscritti: {c[1]}")
            )
        # corsi è una lista. In handlePrintCorsiPD() la lista corsiPD contiene degli oggetti di tipo Corso e quando
        # la stampo sfrutto il metodo __str__ dell'oggetto Corso, che ho scritto appositamente.
        # Qui, la lista corsi contiene tuple: corso + iscritti al quel corso. Dunque, non avendo un __str__
        # definito ad hoc modifico la stampa.
        self._view.update_page()



    def handlePrintIscrittiCodins(self, e):
        self._view.txt_result.controls.clear()
        # self._ddCodinsValue è un oggetto di tipo Corso, che ha fra gli attributi codins.
        # self._ddCodinsValue è una variabile d'appoggio che mi sono creato in _choiceDDCodins nel Controller,
        # è un modo diverso di ottenere il valore del corrispettivo Dropdown
        if self._ddCodinsValue is None:
            self._view.create_alert("Per favore selezionare un insegnamento.")
            self._view.update_page()
            return

        #Se arrivo qui, posso recuperare gli studenti
        studenti = self._model.getStudentiCorso(self._ddCodinsValue.codins)
        # studenti è una lista

        # Se la lista studenti è vuota lo dico all'utente
        if not len(studenti):
            self._view.txt_result.controls.append(
                ft.Text("Nessuno studente iscritto a questo corso."))
            self._view.update_page()
            return

        # Se invece la lista studenti non è vuota la stampo
        self._view.txt_result.controls.append(
            ft.Text(f"Di seguito gli studenti iscritti al corso {self._ddCodinsValue}")
        )
        # Vado a stampare gli studenti (usando __str__ di Studente) contenuti nella lista studenti
        for s in studenti:
            self._view.txt_result.controls.append(
                ft.Text(s)
            )
        self._view.update_page()



    def handlePrintCDSCodins(self, e):
        self._view.txt_result.controls.clear()
        if self._ddCodinsValue is None:
            self._view.create_alert("Per favore selezionare un insegnamento.")
            self._view.update_page()
            return

        cds = self._model.getCDSofCorso(self._ddCodinsValue.codins)

        if not len(cds):
            self._view.txt_result.controls.append(
                ft.Text(f"Nessun CDS afferente al corso {self._ddCodinsValue}"))
            self._view.update_page()
            return

        self._view.txt_result.controls.append(
            ft.Text(f"Di seguito i CDS che frequentano il corso {self._ddCodinsValue}"))

        for c in cds:
            self._view.txt_result.controls.append(ft.Text(f"{c[0]} - N Iscritti: {c[1]}"))
        self._view.update_page()


    # fillddCodins() è il metodo che "riempie" il Dropdown di self.ddCodins nel View.
    # Questo metodo "chiede" al Model la lista di codici di insegnamento,
    # poi cicla su questa lista di codici insegnamento e la aggiunge alla lista delle opzioni del Dropdown.
    # Questo metodo è chiamato nel View.
    def fillddCodins(self):
        # for cod in self._model.getCodins():
        #     self._view.ddCodins.options.append(
        #         ft.dropdown.Option(cod)
        #     )

    # In realtà, conviene leggere il Corso "per intero" invece di leggere solo il suo codins.
        for c in self._model.getAllCorsi():
            self._view.ddCodins.options.append(ft.dropdown.Option(
                key = c.codins,
                data = c,
                on_click = self._choiceDDCodins
            ))
        # - key: è la stringa che viene visualizzata nel menù.
        # - data: associo l'oggetto Corso vero e proprio che sto inserendo nel Dropdown.
        # - on_click funziona come i pulsanti, ma viene attivato quando seleziono l'oggetto che ho selezionato.
        #   Uso on_click tipicamente per salvare da qualche parte nel Controller (in questo caso in _choiceDDCodins)
        #   la voce che è stata selezionata dall'utente.


    def _choiceDDCodins(self, e):
        self._ddCodinsValue = e.control.data
        print(self._ddCodinsValue)
        # Questo metodo legge la selezione dell'utente e la salva in una variabile locale (self_ddCodinsValue).
        # La selezione dell'utente la riesco a prendere dall'evento (e) generato dalla selezione fatta dall'utente.
        # Quindi in questo caso in self_ddCodinsValue c'è l'oggetto di tipo Corso selezionato dall'utente.


    # Nota. I metodi fillddCodins() e _choiceDDCodins() formano un pattern in grado di creare un Dropdown
    # in cui aggiungo degli oggetti, e leggo anche gli oggetti che l'utente ha selezionato dal Dropdown.
    # L'utente a display vedrà la stringa del codins, ma quando seleziona il codins che vuole
    # viene preso tutto l'oggetto di tipo Corso.