import copy

import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self.G = nx.Graph()
        self._artists_list = []
        self.mapA = {}
        self.load_all_artists()

    def load_all_artists(self):
        self._artists_list = DAO.get_all_artists()
        print(f"Artisti: {self._artists_list}")


    def build_graph(self, minAlbum):
        self.m = minAlbum
        self._nodes = DAO.read_specific_artist(minAlbum)
        for artist in self._artists_list:
            self.mapA[artist.id] = artist
        self.G.add_nodes_from(self._nodes)


        lg = {}
        info = DAO.read_edges(minAlbum)
        for i in info:
            if i[0] not in lg.keys():
                lg[i[0]] = set()
                lg[i[0]].add(i[1])
            else:
                lg[i[0]].add(i[1])



        for node1 in self._nodes:
            for node2 in self._nodes:
                if node1 != node2:
                    if not self.G.has_edge(node1, node2):

                        set_generi1 = lg[node1.id]
                        set_generi2 = lg[node2.id]
                        peso = set_generi1.intersection(set_generi2)
                        if len(peso) > 0:
                            self.G.add_edge(node1, node2, weight=len(peso))

    def gestisciC(self, v):
        self.obj_i = self.mapA[v]
        vicini = self.G.neighbors(self.obj_i)
        l = []
        for n in vicini:
          l.append([n, self.G[self.obj_i][n]['weight']])

        sorted_l = sorted(l, key=lambda x: x[1], reverse=False)
        return sorted_l


    def searchpath(self, durata_ms, maxV):
        self.L = maxV
        artistiF_id = DAO.q(durata_ms, self.m)
        self.lista_obj_artisti_filtrati = []
        for a in artistiF_id:
            self.lista_obj_artisti_filtrati.append(self.mapA[a])

        print(self.G.nodes)
        print(self.lista_obj_artisti_filtrati)

        self.soluzione = 0
        self.peso_ottimale = 0
        v = set()
        v.add(self.obj_i)
        self.rec(self.obj_i, [self.obj_i], v, 0)

        return self.soluzione, self.peso_ottimale



    def rec(self, nodoS, parziale, visitati, peso ):
        if len(parziale) == self.L:
            if peso > self.peso_ottimale:
                self.peso_ottimale = peso
                self.soluzione = copy.deepcopy(parziale)
            return
        else:
            for n in self.G.neighbors(nodoS):
                if n not in visitati and n in self.lista_obj_artisti_filtrati:
                    pp = self.G[nodoS][n]['weight']
                    parziale.append(n)
                    visitati.add(n)
                    self.rec(n, parziale, visitati, peso+int(pp))
                    parziale.pop()
                    visitati.remove(n)








