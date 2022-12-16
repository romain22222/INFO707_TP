from mpi4py import MPI

# To launch : mpiexec -n <nb_process> py ./main.py
# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()

new_comm = None
new_rank = None

capteurs = range(0, 4)
collecteurs = range(4, 7)
controleur = [7]
horloge = [8]
bdc = [9]

nb_process = len(capteurs) + len(collecteurs) + len(controleur) + len(horloge) + len(bdc)
if comm.Get_size() != nb_process:
    if rank == 0:
        print("Erreur : pas le bon nombre de processus")
        print(f"Utilisation : mpiexec -n {nb_process} py ./main.py")
    exit(1)


def managerPrincipal():
    print("I am the main manager")


def capteur():
    print("I am a capteur")
    communication = ""
    comm.Recv(communication, source=collecteurs)


def collecteur():
    print("I am a collecteur")


def controlleur():
    print("I am a controlleur")


def h():
    print("I am a horloge")


def barredc():
    print("I am a barre de controle")


def main():
    color = 0 if rank in capteurs else 99
    color = 1 if rank in collecteurs else color
    color = 2 if rank in controleur else color
    color = 3 if rank in horloge else color
    color = 4 if rank in bdc else color
    new_comm = comm.Split(color, rank)
    new_comm.Set_name(str(color))
    new_rank = new_comm.Get_rank()
    print(new_comm.Get_name(), new_rank)
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
    else:
        print("I am process {}".format(rank))


if __name__ == '__main__':
    main()
