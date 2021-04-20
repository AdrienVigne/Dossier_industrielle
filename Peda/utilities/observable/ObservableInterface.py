from threading import Thread

from Peda.utilities.observateur.Observateur import Observer


class ClientObservable:
    '''
    Classe de définition du type observable
    :ivar 'observers' : la liste de tous les observers
    :ivar 'event' : permet de définir l'évènement qui a était déclenché.
    :ivar 'nom' : nom du système observable
    :ivar 'etat' : permet de connaitre l'état du systeme pour l'observateur
    :ivar valeurs : liste permettant de stocker les valeurs qui seront lu par le l'observateur
    :ivar message : Moyen d'informer l'observateur
    '''

    def __init__(self, parent=None):
        #super(ClientObservable, self).__init__(parent)
        ############ variables pour le type observable
        self.list_observers = []
        self.event = ""
        self.nom = "Client"
        self.etat: str = "Non initialisé"
        self.valeurs = []
        self.message = ""
        ########

    def run(self):
        pass

    def get_message(self):
        return self.message

    def get_etat(self):
        return self.etat

    def get_event(self):
        return self.event

    def get_nom(self):
        return self.nom

    def get_valeurs(self):
        return self.valeurs

    def set_nom(self, nom):
        self.nom = nom

    def get_observers(self):
        return self.list_observers

    def add_observer(self, obs: Observer):
        if not hasattr(obs, 'update'):
            raise ValueError("First argument must be object with notify method")
        self.list_observers.append(obs)
        self.notify_observer("add user")

    def delete_observer(self, obs: Observer):
        if obs in self.list_observers:
            self.list_observers.remove(obs)

    def is_registered_observer(self, obs: Observer):
        if obs in self.list_observers:
            return True
        else:
            return False

    def is_observable(self):
        return True

    def notify_observer(self, event: str):
        self.event = event
        for obs in self.list_observers:
            thread = Thread(target=obs.update, args=(self,))
            thread.start()
