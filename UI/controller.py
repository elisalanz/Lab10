import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._selectedCountry = None

    def handleCalcola(self, e):
        anno = self._view._txtAnno.value
        if anno == "":
            self._view.create_alert("Inserire un anno.")
            return
        try:
            anno_int = int(anno)
        except ValueError:
            self._view.create_alert("Usare un formato valido.")
            return
        if anno_int < 1816 or anno_int > 2016:
            self._view.create_alert("Inserire un anno compreso tra 1816 e 2016.")
            return
        self._selectedCountry = None
        self._model.buildGraph(anno_int)
        for country in self._model.getAllCountriesOfYear(anno_int):
            self._view._ddStati.options.append(ft.dropdown.Option(data = country, text = country.StateNme, on_click = self.readDDCountries))
        self._view._btnStatiRaggiungibili.disabled = False
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view._txt_result.controls.append(ft.Text(f"Il grafo ha {self._model.getNumComponentiConn()} componenti connesse."))
        self._view._txt_result.controls.append(ft.Text("Di seguito il dettaglio sui nodi:"))
        nodi_vicini = self._model.getDetailsNodes()
        for nodo in nodi_vicini:
            self._view._txt_result.controls.append(ft.Text(f"{nodo[0]} -- {nodo[1]} vicini."))
        self._view.update_page()

    def readDDCountries(self, e):
        if e.control.data is None:
            self._selectedCountry = None
        else:
            self._selectedCountry = e.control.data

    def handleStatiRaggiungibili(self, e):
        if self._selectedCountry is None:
            self._view.create_alert("Selezionare uno Stato.")
            return
        raggiungibili = self._model.getRaggiungibili(self._selectedCountry)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"{self._selectedCountry} ha {len(raggiungibili)} Stati raggiungibili."))
        if len(raggiungibili)>0:
            self._view._txt_result.controls.append(ft.Text("Di seguito, l'elenco:"))
            for nodo in raggiungibili:
                self._view._txt_result.controls.append(ft.Text(f"{nodo.StateNme}"))
        self._view.update_page()