from multiprocessing import Process

import paho.mqtt.client as mqtt

broker_address = "localhost"
topic = "delta_1"
collector_count = 3
outCollector = "outCollector"

voyant = "vert"
barre = False

diagnosReceived = [0 for i in range(collector_count)]
possiblesDiagnos = ["TEMPERATURE NORMALE", "DEFAILLANCE CAPTEUR", "ALARME TEMPERATURE"]

def controller_loop():
    client = mqtt.Client()
    client.connect(broker_address)
    client.subscribe(topic)
    client.subscribe(outCollector)

    def on_connect(client, userdata, flags, rc):
        print(f"Controller connected with result code {str(rc)}")

    def on_message(client, userdata, msg):
        global voyant, barre, diagnosReceived
        if msg.topic == topic:
            # Analyse les états actuels
            if 2 in diagnosReceived:
                # ALERTE
                barre = True
                voyant = "rouge"
            elif diagnosReceived.count(1) >= 2:
                # WEIRDOS
                barre = True
                voyant = "orange"
            elif 1 in diagnosReceived:
                # BIZARRE MAIS BON
                barre = False
                voyant = "orange"
            else:
                # RAS
                barre = False
                voyant = "vert"
            print(f"Controller sous état : voyant = {voyant} | barres = {'Abaissées' if barre else 'Relevées'}")
        elif msg.topic == outCollector:
            # Récupère l'état d'un collecteur
            data = msg.payload.decode().split("|")
            diagnosReceived[int(data[0])] = possiblesDiagnos.index(data[1])
            # print(f"Controller received {msg.payload.decode()} from {msg.topic}")

    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()


controller_process = Process(target=controller_loop)
controller_process.start()
