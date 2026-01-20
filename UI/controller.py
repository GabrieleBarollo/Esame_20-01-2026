import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_create_graph(self, e):
        global value
        try:
            value = int(self._view.txtNumAlbumMin.value)
            if value <= 0:
                self._view.create_alert("Inserire un numero valido")
        except ValueError:
            self._view.create_alert("Inserire un numero valido")

        self._model.build_graph(value)
        self._view.txt_result.clean()
        self._view.txt_result.controls.append(ft.Text(f"Il grafo è stato creato: {self._model.G}"))

        self._view.ddArtist.disabled = False
        self._view.btnArtistsConnected.disabled = False
        for node in self._model.G.nodes:
            self._view.ddArtist.options.append(ft.dropdown.Option(text=node.name, key = node.id))



        self._view.update_page()




    def handle_connected_artists(self, e):

        v = int(self._view.ddArtist.value)
        i = self._model.gestisciC(v)
        self._view.txt_result.clean()
        self._view.txt_result.controls.append(ft.Text(f"I vicini sono"))
        for d in i:
            self._view.txt_result.controls.append(ft.Text(f"{d[0]}, peso: {d[1]}"))

        self._view.txtMaxArtists.disabled = False
        self._view.txtMinDuration.disabled = False
        self._view.btnSearchArtists.disabled = False
        self._view.update_page()

    def handle_f(self, e):
        global durata_ms, maxV
        try:
            durata_ms = float(self._view.txtMinDuration.value) * 60 * 1000
            maxV = int(self._view.txtMaxArtists.value)
            if durata_ms <= 0 or maxV < 1 or maxV > len(self._model.G.nodes):
                self._view.create_alert("Inserire un numero valido")
        except ValueError:
            self._view.create_alert("Inserire un numero valido")

        percorso, p = self._model.searchpath(durata_ms, maxV)
        self._view.txt_result.clean()
        self._view.txt_result.controls.append(ft.Text(f"Cammino di peso max dall'artista: {self._model.obj_i}"))
        self._view.txt_result.controls.append(ft.Text(f"Lunghezza: {maxV}"))
        for i in percorso:
            self._view.txt_result.controls.append(ft.Text(f" {i}"))
        self._view.txt_result.controls.append(ft.Text(f"peso max : {p}"))
        self._view.update_page()











