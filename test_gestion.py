from multiprocessing import Process

from pynput.keyboard import Key, Controller, Listener, KeyCode
import paho.mqtt.client as mqtt

broker_address = "localhost"
temperatureReactor = 40
proba_success = 0.9
proba_on_remaining_state_wrong_value = 0.5
paused = False

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

    def on_release(key):
        global temperatureReactor, proba_success, proba_on_remaining_state_wrong_value, paused
        key_pressed = False
        if key == KeyCode.from_char('z'):
            key_pressed = True
            temperatureReactor += 1
            client.publish(editTemp, str(temperatureReactor))
        if key == KeyCode.from_char('s'):
            key_pressed = True
            temperatureReactor -= 1
            client.publish(editTemp, str(temperatureReactor))
        if key == KeyCode.from_char("e"):
            key_pressed = True
            proba_success += 0.05 if proba_success < 1 else 0
            client.publish(editPS, str(proba_success))
        if key == KeyCode.from_char('d'):
            key_pressed = True
            proba_success -= 0.05 if proba_success > 0 else 0
            client.publish(editPS, str(proba_success))
        if key == KeyCode.from_char("r"):
            key_pressed = True
            proba_on_remaining_state_wrong_value += 0.05 if proba_on_remaining_state_wrong_value < 1 else 0
            client.publish(editPF, str(proba_on_remaining_state_wrong_value))
        if key == KeyCode.from_char("f"):
            key_pressed = True
            proba_on_remaining_state_wrong_value -= 0.05 if proba_on_remaining_state_wrong_value > 0 else 0
            client.publish(editPF, str(proba_on_remaining_state_wrong_value))
        if key == KeyCode.from_char('p'):
            key_pressed = True
            paused = not paused
            client.publish(pause, "On change la pause")
        if key_pressed:
            print("Nouvel état | Température réacteur :", temperatureReactor,
                  "| Probabilité de bonne mesure :", 100*proba_success,
                  "% | Probabilité de mauvaise mesure :", 100*(1-proba_success)*proba_on_remaining_state_wrong_value,
                  "% | Probabilité de pas de mesure : ", 100*(1-proba_success)*(1-proba_on_remaining_state_wrong_value),
                  "% | En pause :", "Oui" if paused else "Non")

    def on_press(_):
        return

    with Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()


captor_process = Process(target=gestion_loop)
captor_process.start()
