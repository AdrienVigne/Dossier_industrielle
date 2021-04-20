from Peda.utilities.observateur.Observateur import Observer


class Traitement(Observer):

    def __init__(self):
        super(Traitement, self).__init__()

    def update(self, subject) -> None:
        print(f'event : {subject.event}  \n Topic : {subject.valeurs.topic} \n payload : {subject.valeurs.payload.decode()} \n ')
