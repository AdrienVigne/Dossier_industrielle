import threading

from bluepy.btle import Scanner, DefaultDelegate

from gateway.observable.ObservableInterface import ClientObservable
from gateway.observateur import Observateur


class ScannerInterface(DefaultDelegate, ClientObservable):

    def __init__(self, Liste=None):
        super(ScannerInterface, self).__init__()
        DefaultDelegate.__init__(self)
        ClientObservable.__init__(self)




        self.deviceToScan = Liste

    def handleDiscovery(self, scanEntry, isNewDev, isNewData):
        if self.deviceToScan:
            if scanEntry in self.deviceToScan:
                if isNewData:
                    self.message = scanEntry.rawData
                    self.notify_observer("new data")

        else:
            self.message = scanEntry.rawData
            self.notify_observer("device_scanned")


class ClientScanner(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

        #print("Creation")
        self.ScannerDelegate = ScannerInterface()

        self.scanner = Scanner().withDelegate(self.ScannerDelegate)

    def add_observateur(self, obs: Observateur):
        #print(self.__dict__)
        self.ScannerDelegate.add_observer(obs)

    def run(self) -> None:
        if self.ScannerDelegate.list_observers:
            while 1:
                self.scanner.scan()
        else:
            print("Erreur il n'y a personne pour récupérer les infos du scanner")


if __name__ == '__main__':
    pass
