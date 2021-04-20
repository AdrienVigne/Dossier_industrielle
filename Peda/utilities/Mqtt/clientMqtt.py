import paho.mqtt.client as paho

from ..observable.ObservableInterface import ClientObservable
from ..observateur.Observateur import Observer
from ..singleton.singleton import SingletonMeta


class ClientMqtt(Observer, ClientObservable):
    __metaclass__ = SingletonMeta

    def __init__(self, parent=None):
        super(ClientMqtt, self).__init__()
        self.nom = "Client Mqtt"
        self.serveur = "127.0.0.1"
        self.port = 8080
        self.client = paho.Client(self.nom)
        self.client.on_publish = self.onpublish
        self.Debug = True

    def update(self, subject: ClientObservable) -> None:
        if False:
            print(
                f"update de : {subject.nom} \n Evènement recu :{subject.event} \n message : {subject.message} \nvaleurs : {subject.valeurs}")
        self.publish(subject.event, str(subject.message))

    def onpublish(self, client, userdata, result) -> None:
        if self.Debug:
            print(f"Message publié de : {client} avec les données : {userdata}, renvoyant le resultat : {result}")
        else:
            pass

    def connection(self) -> None:
        self.client.connect(self.serveur, self.port, keepalive=3600)
        self.client.on_publish = self.onpublish
        self.client.on_message = self.onmessage

    def publish(self, topic, payload):
        self.client.publish(topic=topic, payload=payload, qos=2)

    def onmessage(self, client, userdata, message):
        self.valeurs = message
        self.notify_observer(message.topic)
