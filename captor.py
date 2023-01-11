import random
from multiprocessing import Process

import paho.mqtt.client as mqtt

broker_address = "localhost"
topic = "captors_topic"
captor_count = 4


def captor_loop(captor_id):
    client = mqtt.Client()
    client.connect(broker_address)
    client.subscribe(topic)

    def on_connect(client, userdata, flags, rc):
        print(f"Collector {captor_id} connected with result code {str(rc)}")

    def on_message(client, userdata, msg):
        if random.random() < 0.001:
            client.publish("collectorChan" + msg.payload.decode(), str(20))

    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()


for captor_id in range(1, captor_count + 1):
    captor_process = Process(target=captor_loop, args=(str(captor_id),))
    captor_process.start()
