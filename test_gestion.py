from multiprocessing import Process

import keyboard
import paho.mqtt.client as mqtt

broker_address = "localhost"
temperatureReactor = 40
proba_success = 0.9
proba_on_remaining_state_wrong_value = 0.5

editPS = "editPS"
editPF = "editPF"
editTemp = "editTemp"
pause = "pause"


def gestion_loop():
    global temperatureReactor, proba_success, proba_on_remaining_state_wrong_value
    client = mqtt.Client()
    client.connect(broker_address)

    def on_connect(_, _userdata, _flags, rc):
        print(f"Gestion connected with result code {str(rc)}")

    client.on_connect = on_connect
    client.loop_start()

    while True:
        if keyboard.is_pressed("z"):
            temperatureReactor += 1
            client.publish(editTemp, str(temperatureReactor))
        if keyboard.is_pressed("s"):
            temperatureReactor -= 1
            client.publish(editTemp, str(temperatureReactor))
        if keyboard.is_pressed("e"):
            proba_success += 0.05 if proba_success < 1 else 0
            client.publish(editPS, str(proba_success))
        if keyboard.is_pressed("d"):
            proba_success -= 0.05 if proba_success > 0 else 0
            client.publish(editPS, str(proba_success))
        if keyboard.is_pressed("r"):
            proba_on_remaining_state_wrong_value += 0.05 if proba_on_remaining_state_wrong_value < 1 else 0
            client.publish(editPF, str(proba_on_remaining_state_wrong_value))
        if keyboard.is_pressed("f"):
            proba_on_remaining_state_wrong_value -= 0.05 if proba_on_remaining_state_wrong_value > 0 else 0
            client.publish(editPF, str(proba_on_remaining_state_wrong_value))
        if keyboard.is_pressed("p"):
            client.publish(pause, "")


captor_process = Process(target=gestion_loop)
captor_process.start()
