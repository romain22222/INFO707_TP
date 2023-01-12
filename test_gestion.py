from multiprocessing import Process

import paho.mqtt.client as mqtt

broker_address = "localhost"
temperatureReactor = 40


def gestion_loop():
    client = mqtt.Client()
    client.connect(broker_address)
    client.subscribe(get_temp)

    def on_connect(client, userdata, flags, rc):
        print(f"Collector {captor_id} connected with result code {str(rc)}")

    def on_message(client, userdata, msg):
        if msg.topic == get_temp:
            client.publish("tempGiven" + msg.payload.decode(), str(20))

    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()


captor_process = Process(target=gestion_loop)
captor_process.start()
