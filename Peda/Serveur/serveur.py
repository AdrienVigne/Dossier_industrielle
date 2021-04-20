from Peda.Serveur.Observateur_traitement import Traitement
from Peda.utilities.Mqtt.clientMqtt import ClientMqtt


class Serveur_traitement:

    def __init__(self):
        super(Serveur_traitement, self).__init__()
        self.clientMQTT = ClientMqtt()
        self.Traitement = Traitement()
        self.clientMQTT.serveur = "192.168.0.2"
        self.clientMQTT.port = 456
        self.clientMQTT.add_observer(self.Traitement)
        self.clientMQTT.connection()

    def run(self):
        self.clientMQTT.run()

