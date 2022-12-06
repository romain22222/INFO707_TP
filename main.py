from mpi4py import MPI
# To launch : mpiexec -n <nb_process> py ./main.py
# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()

print("I am process {}".format(rank))
