import time

from Peda.gateway.Beacon.beacon import Beacon
from Peda.gateway.ble.scannerBle import ClientScanner
from Peda.utilities.Mqtt.clientMqtt import ClientMqtt


class Gateway:

    def __init__(self):
        self.clientMqtt = ClientMqtt()
        self.clientScanner = ClientScanner()
        self.client_beacon = Beacon()
        self.clientMqtt.Debug = True
        self.clientScanner.add_observateur(self.clientMqtt)
        self.clientMqtt.serveur = "192.168.0.2"
        self.clientMqtt.port = 456
        self.clientMqtt.set_nom("Pi0")
        self.clientMqtt.connection()
        self.temps_scan = 10
        self.temps_beacon = 1
        self.temps_pause = 1
        self.clientScanner.run()

    def run(self):
        while 1:
            t = time.time()
            self.clientScanner.unstop()
            while (t - time.time()) < self.temps_scan:
                pass
            self.clientScanner.stop()
            print('Fin scanner')
            t = time.time()
            self.client_beacon.unstop()
            while (t - time.time()) < self.temps_beacon:
                pass
            self.client_beacon.stop()
            print('Fin beacon')
            t = time.time()
            while (t - time.time()) < self.temps_pause:
                pass
            print('Fin pause')


if __name__ == '__main__':
    G = Gateway()

    G.run()
