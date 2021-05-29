import threading

import paho.mqtt.client as paho
from getmac import get_mac_address as gma
from ..observable.ObservableInterface import ClientObservable
from ..observateur.Observateur import Observer
from ..singleton.singleton import SingletonMeta


class ClientMqtt(Observer, ClientObservable, threading.Thread):
    __metaclass__ = SingletonMeta

    def __init__(self, parent=None):
        super(ClientMqtt, self).__init__()
        threading.Thread.__init__(self)
        self.nom = "DefaultClientMqtt"
        self.mac = gma()
        self.serveur = "127.0.0.1"
        self.port = 8080
        self.client = paho.Client(self.nom)

        self.Debug = True
        self.__stop_event = False

    def update(self, subject: ClientObservable) -> None:
        if False:
            print(
                f"update de : {subject.nom} \n Evènement recu :{subject.event} \n message : {subject.message} \nvaleurs : {subject.valeurs}")
        self.publish(f"{self.mac}", str(subject.message))

    def onpublish(self, client, userdata, result) -> None:
        if self.Debug:
            #print(f"Message publié de : {client} avec les données : {userdata}, renvoyant le resultat : {result}")
            pass
        else:
            pass


    def set_nom(self, nom):
        self.client._client_id = nom
        self.nom = nom

    def connection(self) -> None:

        self.client.connect(self.serveur, self.port, keepalive=3600)
        self.client.on_publish = self.onpublish
        self.client.on_message = self.onmessage
        self.client.subscribe(f"{self.mac}/param/#")

    def publish(self, topic, payload):
        if self.Debug:
            print(f"Topic : {topic}, charge utile = {payload}")
        self.client.publish(topic=topic, payload=payload)

    def onmessage(self, client, userdata, message):
        #print("Message recu")
        self.valeurs = message.payload
        self.event = message.topic
        if f"{self.mac}/param/" in message.topic:
            print("message de param : ",message.payload)
        self.notify_observer(message.topic)

    def unstop(self):
        self.__stop_event = True

    def stop(self):
        self.__stop_event = False

    def run(self):
        while 1:
            if self.__stop_event:
                self.client.loop_read()
