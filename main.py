import subprocess
from multiprocessing import Process


def run_script(script):
    subprocess.run(["python", script])


if __name__ == "__main__":
    clock_process = Process(target=run_script, args=("horloge.py",))
    collector_process = Process(target=run_script, args=("collector.py",))
    controller_process = Process(target=run_script, args=("controller.py",))
    captor_process = Process(target=run_script, args=("captor.py",))
    test_gestion_process = Process(target=run_script, args=("test_gestion.py",))

    clock_process.start()
    collector_process.start()
    controller_process.start()
    captor_process.start()
    test_gestion_process.start()
