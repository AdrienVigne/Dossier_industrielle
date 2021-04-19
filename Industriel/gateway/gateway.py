from gateway.Mqtt.clientMqtt import ClientMqtt
from gateway.ble.scannerBle import ClientScanner


class Gateway:

    def __init__(self):
        self.clientMqtt = ClientMqtt()
        self.clientScanner = ClientScanner()
        self.clientMqtt.Debug = True
        self.clientScanner.add_observateur(self.clientMqtt)
        self.clientMqtt.serveur = "192.168.0.2"
        self.clientMqtt.port = 456
        self.clientMqtt.connection()


    def run(self):
        self.clientScanner.run()




if __name__ == '__main__':
    G = Gateway()
    # G.liste_beacon = ["0x:45:78:89:5:2:5"]
    # G.temps_beacon = 25
    # G.temps_scan = 12
    # G.temps_pause = 2
    G.start()
