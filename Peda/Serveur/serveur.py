from Peda.Serveur.Observateur_traitement import Traitement
from Peda.utilities.Mqtt.clientMqtt import ClientMqtt
from Peda.utilities.clientBdd.ClientSql import clientMysql


class Serveur_traitement:

    def __init__(self):
        super(Serveur_traitement, self).__init__()
        self.clientMQTT = ClientMqtt()
        self.clientMQTT.set_nom("Serveur")
        self.Traitement = Traitement()
        self.bdd = clientMysql()
        self.clientMQTT.serveur = "192.168.0.2"
        self.clientMQTT.port = 456
        self.clientMQTT.add_observer(self.Traitement)
        self.clientMQTT.connection()
        self.clientMQTT.client.subscribe('#')



    def run(self):
        self.clientMQTT.run()




if __name__ == '__main__':

    S = Serveur_traitement()
    S.Traitement.add_gate("ac:23:3f:a3:33:d6")

    S.run()
