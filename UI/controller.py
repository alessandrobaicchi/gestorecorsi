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

        self._view.txt_result.controls.clear()

        pd = self._view.ddPD.value

        if pd is None:
            (self._view.create_alert
             ("Attenzione, selezionare un periodo didattico."))
            self._view.update_page()
            return

        if pd == "I":
            pdInt = 1
        else: pdInt = 2

        corsiPD = self._model.getCorsiPD(pdInt)

        if not len(corsiPD):
            self._view.txt_result.controls.append(
                ft.Text(f"Nessun corso trovato per il {pd} periodo didattico."))
            self._view.update_page()
            return

        self._view.txt_result.controls.append(
            ft.Text(f"Di seguito i corsi del {pd} periodo didattico:"))
        for c in corsiPD:
            self._view.txt_result.controls.append(
                ft.Text(c)
            )
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
        self._view.update_page()

    def handlePrintIscrittiCodins(self, e):
        self._view.txt_result.controls.clear()

        if self._ddCodinsValue is None:
            self._view.create_alert("Per favore selezionare un insegnamento.")
            self._view.update_page()
            return

        #se arriviamo qui, posso recuperare gli studenti
        studenti = self._model.getStudentiCorso(self._ddCodinsValue.codins)

        if not len(studenti):
            self._view.txt_result.controls.append(
                ft.Text("Nessuno studente iscritto a questo corso."))
            self._view.update_page()
            return

        self._view.txt_result.controls.append(
            ft.Text(f"Di seguito gli studenti iscritti al corso {self._ddCodinsValue}")
        )
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