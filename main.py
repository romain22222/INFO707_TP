from mpi4py import MPI

# To launch : mpiexec -n <nb_process> py ./main.py
# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()

manager = [0]
capteurs = range(1, 5)
collecteurs = range(5, 8)
controleur = [8]

nb_process = len(manager) + len(capteurs) + len(collecteurs) + len(controleur)
if comm.Get_size() != nb_process:
    if rank == 0:
        print("Erreur : pas le bon nombre de  de processus")
        print(f"Utilisation : mpiexec -n {nb_process} py ./main.py")
    exit(1)


def managerPrincipal():
    print("I am the main manager")


def capteur():
    print("I am a capteur")


def collecteur():
    print("I am a collecteur")


def controlleur():
    print("I am a controlleur")


if rank in manager:
    managerPrincipal()
elif rank in capteurs:
    capteur()
elif rank in collecteurs:
    collecteur()
elif rank in controleur:
    controlleur()
else:
    print("I am process {}".format(rank))
