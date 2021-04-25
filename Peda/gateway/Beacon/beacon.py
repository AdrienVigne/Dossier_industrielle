import os
import threading


class Beacon(threading.Thread):

    def __init__(self):
        super(Beacon, self).__init__()
        self.__stop_event = False
        self.passage = True

    def unstop(self):
        self.__stop_event = True
        self.passage = True

    def stop(self):
        self.__stop_event = False

    def run(self) -> None:
        while 1:
            if not self.__stop_event:
                if self.passage:
                    os.system("sudo hciconfig hci0 up")
                    os.system("sudo hciconfig hci0 leadv 3")
                    os.system(
                        "sudo hcitool -i hci0 cmd 0x08 0x0008 1c 02 01 06 03 03 aa fe 14 16 aa fe 10 00 02 63 69 72 63 75 69 74 64 69 67 65 73 74 07 00 00 00")
                self.passage = False
