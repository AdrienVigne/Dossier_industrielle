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
        self.clientMqtt.add_observer(self.clientScanner)
        self.clientMqtt.serveur = "192.168.0.2"
        self.clientMqtt.port = 456
        self.clientMqtt.set_nom("Pi0")
        self.clientMqtt.connection()
        self.temps_scan = 1
        self.temps_beacon = 0
        self.temps_pause = 10
        self.clientScanner.start()
        self.client_beacon.start()
        self.clientMqtt.start()


    def run(self):
        print("Lancement ")
        while 1:
            print("Debut scan")
            t = time.time()
            self.clientScanner.unstop()
            while (time.time()-t) < self.temps_scan:
                pass
            self.clientScanner.stop()
            print('Fin scanner')
            t = time.time()
            self.client_beacon.unstop()
            while (time.time()-t) < self.temps_beacon:
                pass
            self.client_beacon.stop()
            print('Fin beacon')
            t = time.time()
            self.clientMqtt.unstop()
            while (time.time()-t) < self.temps_pause:
                pass
            self.clientMqtt.stop()
            print('Fin pause')


if __name__ == '__main__':
    G = Gateway()

    G.run()
