import paho.mqtt.client as mqtt
import time

broker_address = "localhost"
delta_1 = "delta_1"
delta_2 = "delta_2"
interval = 1


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


client = mqtt.Client()
client.on_connect = on_connect
client.connect(broker_address)
client.loop_start()

while True:
    client.publish(delta_1, "tick")
    #print("d1 sent")
    for i in range(100):
        client.publish(delta_2, "tick")
     #   print("d2 sent")
        time.sleep(interval / 100)
