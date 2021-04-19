import os
import threading
import time
from bluepy.btle import Scanner, DefaultDelegate
import paho.mqtt.client as paho


class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            #print("Discovered device", dev.addr)
            print(dev.__dict__)
            #print(dev.getScanData())
        elif isNewData:
            print("Received new data from", dev.addr)


class GatewayV1(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.client = None
        self.__adresse_broker = "192.168.0.2"
        self.__port_broker = 456
        self.nom_gateway = "Gatewaypi0"
        self.client = paho.Client(self.nom_gateway)
        self.client.connect(self.__adresse_broker, port=self.__port_broker, keepalive=3600)
        self.client.subscribe(self.nom_gateway + '/#')
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        self.temps_scan = 2
        self.temps_beacon = 10
        self.temps_pause = 2
        self.liste_beacon = ["ac:23:3f:a3:33:db", "ac:23:3f:a3:33:d6", "b8:27:eb:f8:27:74",
                             "b8:27:eb:89:dd:db"]  # db pi3 #74 pi0
        self.adresse_mac = ""
        print("Fin initialisation")

    # -- liste beacon
    @property
    def liste_beacon(self):
        return self.__liste_beacon

    @liste_beacon.setter
    def liste_beacon(self, value):
        self.__liste_beacon = value
        self.publish("liste_beacon", str(self.__liste_beacon))
        pass

    @property
    def temps_scan(self):
        return self.__temps_scan

    @temps_scan.setter
    def temps_scan(self, value):
        self.__temps_scan = value
        self.publish("temps_scan", str(value))
        pass

    @property
    def temps_beacon(self):
        return self.__temps_beacon

    @temps_beacon.setter
    def temps_beacon(self, value):
        self.__temps_beacon = value
        self.publish("temps_beacon", str(value))
        pass

    @property
    def temps_pause(self):
        return self.__temps_pause

    @temps_pause.setter
    def temps_pause(self, value):
        self.__temps_pause = value
        self.publish("temps_pause", str(value))
        pass

    @property
    def nom_gateway(self):
        return self.__nom_gateway

    @nom_gateway.setter
    def nom_gateway(self, value):
        self.__nom_gateway = value
        if self.client is not None:
            self.publish("nom_gateway",value)

    def publish(self, topic: str, value: str):
        self.client.publish(self.nom_gateway + "/" + topic, value)
        time.sleep(0.001)

    def on_publish(self, client, userdata, result):
        print("message envoyer")
        pass

    def on_message(self, client, userdata, message):
        # print("Message recu avec le topic : ",message.topic)
        if message.topic == self.nom_gateway + "/set_liste_beacon":
            msg = message.decode()
            self.liste_beacon = msg.split(";")
        if message.topic == self.nom_gateway + "/set_temps_scan":
            msg = message.payload.decode()
            self.temps_scan = float(msg)
        if message.topic == self.nom_gateway + "/set_temps_beacon":
            msg = message.payload.decode()
            self.temps_beacon = float(msg)
        if message.topic == self.nom_gateway + "/set_temps_pause":
            msg = message.payload.decode()
            self.temps_pause = float(msg)
        if message.topic == self.nom_gateway +"/set_nom_gateway":
            msg = message.payload.decode()
            self.nom_gateway = msg

    def run(self):
        while 1:
            scanner = Scanner().withDelegate(ScanDelegate())
            devices = scanner.scan(self.temps_scan)
            for dev in devices:
                print("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
                if dev.addr in self.liste_beacon:
                    # self.publish("list_device",
                    #              "Pi => Device %s (%s), RSSI=%d dB , Nom = %s" % (
                    #                  dev.addr, dev.addrType, dev.rssi, dev.addr[len(dev.addr) - 6:]))
                    self.publish("list_device",
                                 "%s;%d" % (
                                     dev.addr, dev.rssi))

            T = time.time()
            passage = True

            while time.time() - T < self.temps_beacon:
                if passage:
                    os.system("sudo hciconfig hci0 up")
                    os.system("sudo hciconfig hci0 leadv 3")
                    os.system(
                        "sudo hcitool -i hci0 cmd 0x08 0x0008 1c 02 01 06 03 03 aa fe 14 16 aa fe 10 00 02 63 69 72 63 75 69 74 64 69 67 65 73 74 07 00 00 00")
                    passage = False
            T = time.time()
            while time.time() - T < self.temps_pause:
                self.client.loop_read()
            print("fin de boucle complete")


if __name__ == '__main__':
    G = GatewayV1()
    # G.liste_beacon = ["0x:45:78:89:5:2:5"]
    # G.temps_beacon = 25
    # G.temps_scan = 12
    # G.temps_pause = 2
    G.start()
