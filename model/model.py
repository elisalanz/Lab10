import networkx as nx
from networkx.algorithms.traversal import dfs_tree

from database.DAO import DAO
from database.DB_connect import DBConnect


class Model:

    def __init__(self):
        self._grafo = nx.Graph()
        self._allCountries = []
        self._idMapCountries = {}

    def getAllCountriesOfYear(self, anno):
        countries = DAO.getAllCountries(anno)
        for country in countries:
            self._idMapCountries[country.CCode] = country
        countries.sort(key=lambda x: x.StateNme)
        return countries

    def buildGraph(self, anno):
        self._grafo.clear()
        self._idMapCountries = {}
        self._allCountries = self.getAllCountriesOfYear(anno)
        if len(self._allCountries) == 0:
            print("Lista Stati vuota")
            return
        self._grafo.add_nodes_from(self._allCountries)
        edges = DAO.getAllEdges(anno, self._idMapCountries)
        self._grafo.add_edges_from(edges)

    def getDetailsNodes(self):
        details = [] # lista di tuple (nome_stato, num_vicini)
        nodes = self._grafo.nodes()
        for node in nodes:
            details.append((node.StateNme, self._grafo.degree(node)))
        details.sort(key=lambda x: x[0])
        return details

    def getNumComponentiConn(self):
        return nx.number_connected_components(self._grafo)

    def getRaggiungibili(self, nodo):
        raggiungibili = []
        comp_connessa = dfs_tree(self._grafo, nodo)
        raggiungibili.extend(comp_connessa.nodes())
        raggiungibili.remove(nodo)
        raggiungibili.sort(key=lambda x: x.StateNme)
        return raggiungibili
