import threading

from bluepy.btle import Scanner, DefaultDelegate

from Peda.utilities.observable.ObservableInterface import ClientObservable
from Peda.utilities.observateur.Observateur import Observer


class ScannerInterface(DefaultDelegate, ClientObservable):

    def __init__(self, Liste=None):
        super(ScannerInterface, self).__init__()
        DefaultDelegate.__init__(self)
        ClientObservable.__init__(self)

        self.deviceToScan = Liste
        self.minRSSI = -60

    def handleDiscovery(self, scanEntry, isNewDev, isNewData):
        if self.deviceToScan:
            if scanEntry.addr in self.deviceToScan:
                if scanEntry.rssi > self.minRSSI:
                    self.message = [scanEntry.addr, scanEntry.rssi]
                    self.notify_observer("device_scanned")
        else:
            self.message = [scanEntry.addr, scanEntry.rssi]
            self.notify_observer("device_scanned")


class ClientScanner(threading.Thread, Observer):

    def __init__(self):
        threading.Thread.__init__(self)
        # print("Creation")
        self.ScannerDelegate = ScannerInterface(['ac:23:3f:a3:33:d8'])
        self.scanner = Scanner().withDelegate(self.ScannerDelegate)
        self.__stop_event = False

    def add_observateur(self, obs: Observer):
        # print(self.__dict__)
        self.ScannerDelegate.add_observer(obs)

    def unstop(self):
        self.__stop_event = True
        print("Lancement")

    def stop(self):
        self.__stop_event = False

    def update(self, subject: ClientObservable) -> None:
        print("update client scanner")
        param = subject.event.split('/')[-1]
        print(param)
        if param == 'add_device':
            new_device = eval(subject.valeurs.decode())
            print(new_device)
            if new_device not in self.ScannerDelegate.deviceToScan:
                self.ScannerDelegate.deviceToScan.append(new_device)
            print(self.ScannerDelegate.deviceToScan)
        if param == 'set_min_rssi':
            rssi = eval(subject.valeurs.decode())
            print('new rssi min :',rssi)
            self.ScannerDelegate.minRSSI = rssi
            print(self.ScannerDelegate.minRSSI)


    def run(self) -> None:
        if self.ScannerDelegate.list_observers:
            while 1:
                if self.__stop_event:
                    self.scanner.scan()
        else:
            print("Erreur il n'y a personne pour récupérer les infos du scanner")


if __name__ == '__main__':
    pass
