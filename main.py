import keyboard
from mpi4py import MPI

# To launch : mpiexec -n <nb_process> py ./main.py
# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()

new_comm = None
new_rank = None

# les differents range des ranks
capteurs = range(0, 4)
collecteurs = range(4, 7)
controleur = [7]
horloge = [8]
bdc = [9]
console = [10]

nb_process = len(capteurs) + len(collecteurs) + len(controleur) + len(horloge) + len(bdc) + len(console)
if comm.Get_size() != nb_process:
    if rank == 0:
        print("Erreur : pas le bon nombre de processus")
        print(f"Utilisation : mpiexec -n {nb_process} py ./main.py")
    exit(1)

"""
capteur = 4
collecteur = 3

preRequis : les collecteurs demandent aux capteurs de leur envoyer des données
obj : envoye des valeur entre les 4 processus de capteur aux trois aux processus de collecteur

"""


def capteur():
    print("I am a capteur")
    while 1:
        value = comm.recv(tag=rank)
        print(value)
        comm.send(str(20), dest=int(str(value).split("ask data ")[1]),
                  tag=int(str(value).split("ask data ")[1]))


def collecteur():
    print("I am a collecteur")
    while 1:
        for j in capteurs:
            comm.send("ask data " + str(rank), dest=j, tag=j)
        for j in capteurs:
            data = comm.recv(source=j)
            print(str(j) + data)


def controlleur():
    print("I am a controlleur")


def h():
    print("I am a horloge")


def barredc():
    print("I am a barre de controle")


def upTemp():
    # est censé augmenter de 1 la température
    return


def cons():
    print("I am the console")
    while True:
        if keyboard.read_key() == "p":
            print("coucou")
            upTemp()


def main():
    if rank in capteurs:
        capteur()
    elif rank in collecteurs:
        collecteur()
    elif rank in controleur:
        controlleur()
    elif rank in horloge:
        h()
    elif rank in bdc:
        barredc()
    elif rank in console:
        cons()
    else:
        print("I am process {}".format(rank))


if __name__ == '__main__':
    main()
