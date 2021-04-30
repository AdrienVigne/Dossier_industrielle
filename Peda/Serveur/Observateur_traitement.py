import threading

import numpy as np
from numpy import mean
from scipy import minimize

from Peda.utilities.Mqtt import clientMqtt
from Peda.utilities.clientBdd.ClientSql import clientMysql
from Peda.utilities.observateur.Observateur import Observer


class Traitement(Observer, threading.Thread):

    def __init__(self):
        super(Traitement, self).__init__()
        self.liste_beacon = ["ac:23:3f:a3:33:db"]
        self.liste_gateway = ["ac:23:3f:a3:33:d6"]
        self.bdd = clientMysql()
        self.liste_position = {}
        self.calcul = {}
        self.new_gateway = None
        self.new_device = None

    def update(self, subject: clientMqtt) -> None:
        # print(
        #    f'event : {subject.event}  \n Topic : {subject.valeurs.topic} \n payload : {subject.valeurs.payload.decode()} \n ')

        Val = []
        try:
            Val = eval(subject.valeurs.payload.decode())
            # print('Val : ',Val,'type VAl : ',type(Val))
        except:
            pass
        if len(Val) == 2:

            dev = Val[0]
            rssi = Val[1]
            gate = subject.event
            if gate not in self.calcul.keys():
                # print('element pas le dictionnaire des gateway')
                self.calcul[gate] = {}
            if dev in self.liste_gateway:
                self.traitement_gateway(gate, dev, rssi)
            if dev in self.liste_beacon:
                self.traitement_beacon(gate, dev, rssi)

                print(self.calcul)

            # print("Mise a jour de la valeurs")
            # print(self.list_val)
            # self.list_val[gate][dev].append(rssi)
            # self.bdd.ajout_rssi(gate, dev, rssi)

    def calcul_localisation(self, dev,list_gateway):

    def calcul_cout(self, position, dev, list_gate):
        n = 0
        c = 0
        for gate in list_gate:
            c += (self.calcul[gate][dev]["Distance"][-1] - self.distance(position, gate)) ^ 2
            n += 1
        return c / n

    def distance(self, position, gate):
        if gate in self.liste_position:
            gate_position = np.array([self.liste_position[gate]['x'], self.liste_position[gate]['y']])
            dist = np.linalg.norm(gate_position - position)
            return dist
        else:
            self.add_gate(gate)
            self.distance(position, gate)
        pass

    def traitement_beacon(self, gate, dev, rssi):
        if dev in self.calcul[gate].keys():
            self.calcul[gate][dev]['Rssi'].append(rssi)
        else:
            print("new beacon")
            self.calcul[gate][dev] = {'Rssi': [rssi], 'Distance': []}
            self.liste_position[dev] = [np.array([0, 0])]
        if 'Mean_coef' in self.calcul[gate].keys():
            self.calcul[gate][dev]['Distance'].append(rssi * self.calcul[gate]['Mean_coef'])
            self.ajout_localisation(dev)

    def traitement_gateway(self, gate, dev, rssi):
        if dev in self.calcul[gate].keys():
            self.calcul[gate][dev]['Rssi'].append(rssi)
            self.calcul[gate][dev]['Rssi_moyen'] = mean(self.calcul[gate][dev]['Rssi'])
            self.calcul[gate][dev]['Coef'] = self.calcul[gate][dev]['Distance'] / \
                                             self.calcul[gate][dev]['Rssi_moyen']
            coefMean = 0
            N_gateway = 0
            for gate2 in self.calcul[gate].keys():
                if gate2 in self.liste_gateway:
                    coefMean = coefMean + self.calcul[gate][gate2]['Coef']
                    N_gateway += 1
            self.calcul[gate]['Mean_coef'] = coefMean
            self.calcul[gate]['N_gateway'] = N_gateway
            D = self.distance_gateway(gate, dev)
            if D != self.calcul[gate][dev]['Distance']:
                self.calcul[gate][dev]['Distance'] = D
        else:
            print("New gateway")
            Distance = self.distance_gateway(gate, dev)
            self.calcul[gate][dev] = {'Rssi': [rssi], 'Distance': Distance, 'Rssi_moyen': rssi,
                                      'Coef': Distance / rssi}

    def run(self):
        while 1:
            pass

    def add_gate(self, gate):
        G = self.bdd.get_position(gate)
        self.liste_position[gate] = {'x': G[0], 'y': G[1]}
        pass

    def distance_gateway(self, gate1, gate2):
        if gate1 in self.liste_position:
            if gate2 in self.liste_position:
                g1 = np.array([self.liste_position[gate1]['x'], self.liste_position[gate1]['y']])
                g2 = np.array([self.liste_position[gate2]['x'], self.liste_position[gate2]['y']])
                d = np.linalg.norm(g1 - g2)
                return d
            else:
                self.add_gate(gate2)
                self.distance_gateway(gate1, gate2)
        else:
            self.add_gate(gate1)
            self.distance_gateway(gate1, gate2)

    def ajout_localisation(self, dev):
        list_gateway = []
        for gate in self.calcul.keys():
            if dev in self.calcul[gate].keys():
                list_gateway.append(gate)
        if len(list_gateway) >= 3:
            pos = minimize(self.calcul_cout, self.liste_position[dev][-1], args=(dev, list_gateway))
            print(pos.x)
            self.liste_position[dev].append(pos.x)

        pass
