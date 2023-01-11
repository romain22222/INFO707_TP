from multiprocessing import Process

import paho.mqtt.client as mqtt

broker_address = "localhost"
delta_1 = "delta_1"
delta_2 = "delta_2"
collector_count = 3
captor_count = 4
captor_topic = "captors_topic"
collectorChanGeneral = "collectorChan"
outCollector = "outCollector"

tabCheckReceived = [[False for _ in range(captor_count)] for _ in range(collector_count)]
vals = [[0 for _ in range(captor_count)] for _ in range(collector_count)]
gotDelta2 = [False for _ in range(collector_count)]

seuil = 30


def collector_loop(collector_id):
    global tabCheckReceived, vals
    client = mqtt.Client()
    client.connect(broker_address)
    client.subscribe(delta_1)
    client.subscribe(collectorChanGeneral + collector_id)
    intCollectorId = int(collector_id)

    def on_connect(client, userdata, flags, rc):
        print(f"Collector {collector_id} connected with result code {str(rc)}")

    def on_message(client, userdata, msg):
        if msg.topic == delta_1:
            tabCheckReceived[intCollectorId] = [False] * captor_count
            vals[intCollectorId] = [0] * captor_count
            # print(f"Collector {collector_id} received tick")
            for captor_id in range(1, captor_count + 1):
                client.publish(captor_topic, collector_id)
            client.subscribe(delta_2)
        elif msg.topic == collectorChanGeneral + collector_id:
            data = msg.payload.decode().split('|')
            captor = int(data[0])
            valeur = int(data[1])
            tabCheckReceived[intCollectorId][captor] = True
            vals[intCollectorId][captor] = valeur
            # print(f"Collector {collector_id} recoit la donnée du capteur {captor} : {valeur}")
        elif msg.topic == delta_2:
            if gotDelta2[intCollectorId]:
                client.unsubscribe(delta_2)
                gotDelta2[intCollectorId] = False
                valsSet = set(vals[intCollectorId])
                if len([v for v in tabCheckReceived[intCollectorId] if v]) < captor_count-1:
                    client.publish(outCollector, collector_id + "|DEFAILLANCE CAPTEUR")
                elif any(vals[intCollectorId].count(list(valsSet)[i]) >= 3 for i in range(len(valsSet))):
                    # Valeur fiable pour sur
                    vToCheck = vals[intCollectorId][[i for i in range(len(valsSet)) if vals[intCollectorId].count(list(valsSet)[i]) >= 3][0]]
                    client.publish(outCollector, collector_id + ("|ALARME TEMPERATURE" if vToCheck < seuil else "|TEMPERATURE NORMALE"))
                else:
                    # Choke pas de valeur fiable
                    client.publish(outCollector, collector_id + "|DEFAILLANCE CAPTEUR")
            else:
                gotDelta2[intCollectorId] = True

    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()


for collector_id in range(collector_count):
    collector_process = Process(target=collector_loop, args=(str(collector_id),))
    collector_process.start()
