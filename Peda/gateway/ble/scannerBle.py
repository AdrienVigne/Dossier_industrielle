import threading

from bluepy.btle import Scanner, DefaultDelegate

from Peda.utilities.observable.ObservableInterface import ClientObservable
from Peda.utilities.observateur import Observateur


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
            self.message = [scanEntry.addr,scanEntry.rssi]
            self.notify_observer("device_scanned")


class ClientScanner(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        # print("Creation")
        self.ScannerDelegate = ScannerInterface()
        self.scanner = Scanner().withDelegate(self.ScannerDelegate)
        self.__stop_event = False

    def add_observateur(self, obs: Observateur):
        # print(self.__dict__)
        self.ScannerDelegate.add_observer(obs)

    def unstop(self):
        self.__stop_event = True

    def stop(self):
        self.__stop_event = False

    def run(self) -> None:
        if self.ScannerDelegate.list_observers:
            while 1:
                if not self.__stop_event:
                    self.scanner.scan()
        else:
            print("Erreur il n'y a personne pour récupérer les infos du scanner")


if __name__ == '__main__':
    pass
