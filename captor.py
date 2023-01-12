import random
from multiprocessing import Process

import paho.mqtt.client as mqtt

broker_address = "localhost"
captors_topic = "captors_topic"
captor_count = 4

proba_success = 0.9
proba_on_remaining_state_wrong_value = 0.5
actual_temperature = 40

editPS = "editPS"
editPF = "editPF"
editTemp = "editTemp"


def captor_loop(captor_id):
    client = mqtt.Client()
    client.connect(broker_address)
    client.subscribe(captors_topic)

    def on_connect(_, userdata, flags, rc):
        print(f"Collector {captor_id} connected with result code {str(rc)}")

    def on_message(clientMsg, userdata, msg):
        global actual_temperature, proba_success, proba_on_remaining_state_wrong_value
        if msg.topic == captors_topic:
            if random.random() < proba_success:
                clientMsg.publish("collectorChan" + msg.payload.decode(), captor_id + "|" + str(actual_temperature))
            elif random.random() < proba_on_remaining_state_wrong_value:
                clientMsg.publish("collectorChan" + msg.payload.decode(), captor_id + "|" + str(actual_temperature))
        elif msg.topic == editTemp:
            actual_temperature = int(msg.payload.decode())
        elif msg.topic == editPS:
            proba_success = float(msg.payload.decode())
        elif msg.topic == editPF:
            proba_on_remaining_state_wrong_value = float(msg.payload.decode())

    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()


for captor_id in range(1, captor_count + 1):
    captor_process = Process(target=captor_loop, args=(str(captor_id),))
    captor_process.start()
