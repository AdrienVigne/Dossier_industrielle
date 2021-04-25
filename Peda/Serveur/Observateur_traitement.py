
import threading

from Peda.utilities.Mqtt import clientMqtt
from Peda.utilities.clientBdd.ClientSql import clientMysql
from Peda.utilities.observateur.Observateur import Observer


class Traitement(Observer,threading.Thread):

    def __init__(self):
        super(Traitement, self).__init__()
        self.bdd = clientMysql()
        self.list_val = {}
        self.list_fig = {}
        self.new_gateway = None
        self.new_device = None

    def update(self, subject: clientMqtt) -> None:
        # print(
        #    f'event : {subject.event}  \n Topic : {subject.valeurs.topic} \n payload : {subject.valeurs.payload.decode()} \n ')

        Val = []
        try:
            Val = eval(subject.valeurs.payload.decode())
            # print('Val : ',Val,'type VAl : ',type(Val))
        except:
            pass
        if len(Val) == 2:
            if subject.event not in self.list_val:
                # print('element pas le dictionnaire des gateway')
                self.list_val[subject.event] = {}
                self.new_gateway = subject.event
            if Val[0] not in self.list_val[subject.event]:
                # print("Nouveau periphérique detecter par la gateway")
                self.list_val[subject.event][Val[0]] = []
                self.new_device = Val[0]
            # print("Mise a jour de la valeurs")
            # print(self.list_val)
            self.list_val[subject.event][Val[0]].append(Val[1])
            self.bdd.ajout_rssi(subject.event,Val[0],Val[1])






    def animate(self,gate):
        [fig, ax] = self.list_fig[gate]
        ax.clear()
        plt.title(gate)
        for dev, list_rssi in dict_gate.items():
            ax.plot(list_rssi, label=dev)
        plt.legend()
    def affichage(self):
        if self.new_gateway is not None:
            print("Nouvelle figure")
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
            anim = animation.FuncAnimation(fig,self.animate,fargs=(self,self.new_gateway),interval=1000,blit=True)
            self.list_fig[self.new_gateway] = [fig, ax,anim]
        plt.show()

    def run(self):
        while 1:
            self.affichage()

        # for gate, dict_gate in self.list_val.items():
        #     for dev, list_rssi in dict_gate.items():
        #         [fig, ax] = self.list_fig[gate]
        #         fig.title(gate)
        #         ax.clear()
        #         ax.plot(list_rssi, label=dev)
        # plt.show()


    # def affichage(self):
    #     plt.close('all')
    #     i = 1
    #     if self.list_val != {}:
    #         try:
    #             for key, val in self.list_val.items():
    #                 plt.fig(i)
    #                 i = i + 1
    #                 plt.title(key)
    #                 for dev, list in self.list_val[key].items():
    #                     print("dev : ", dev, 'list : ', list)
    #                     plt.plot(list, label=dev)
    #
    #
    #         except:
    #             pass
    #     plt.legend()
    #     plt.show()
