import time

import paho.mqtt.client as mqtt

broker_address = "localhost"
delta_1 = "delta_1"
delta_2 = "delta_2"
interval = 1

pause = "pause"

isPaused = False


def on_connect(_, _userdata, _flags, rc):
    print("Connected with result code " + str(rc))


def on_message(_, _userdata, msg):
    global isPaused
    if msg.topic == pause:
        isPaused = not isPaused


client = mqtt.Client()
client.on_connect = on_connect
client.connect(broker_address)
client.loop_start()

while True:
    client.publish(delta_1, "tick")
    # print("d1 sent")
    for i in range(100):
        while isPaused:
            continue
        client.publish(delta_2, "tick")
        #   print("d2 sent")
        time.sleep(interval / 100)
