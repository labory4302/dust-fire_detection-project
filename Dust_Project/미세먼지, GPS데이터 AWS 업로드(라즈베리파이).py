import time, json, ssl
import paho.mqtt.client as mqtt
import serial

ENDPOINT = 'aakgta5gjm8co-ats.iot.us-west-2.amazonaws.com'
THING_NAME = 'test-thing'
ser = serial.Serial('/dev/ttyACM1',9600)



def on_connect(mqttc, obj, flags, rc):
	if rc == 0: # 연결 성공
		print('connected!!')
		mqttc.subscribe('test/2', qos=0) # 구독

def on_message(mqttc, obj, msg):
	if msg.topic == 'test/2':
		payload = msg.payload.decode('utf-8')
		j = json.loads(payload)
		print(j['message'])

mqtt_client = mqtt.Client(client_id=THING_NAME)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.tls_set('./certs/root1.pem', certfile='./certs/root.pem.crt',
	keyfile='./certs/root2.pem.key', tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
mqtt_client.connect(ENDPOINT, port=8883)
mqtt_client.loop_start() # threaded network loop


while True:
    Now = time.localtime()
    Real_Year = str(Now.tm_year)
    Real_Month = str(Now.tm_mon)
    Real_Day = str(Now.tm_mday)
    Real_Hour = str(Now.tm_hour)
    Real_Minute = str(Now.tm_min)
    Real_Second = str(Now.tm_sec)
    Real_Time_Data = '"Date" : "'+Real_Year+'/'+Real_Month+'/'+Real_Day+'", "Time" : "'+Real_Hour+':'+Real_Minute+':'+Real_Second+'"'

    line = ser.readline()
    NLLFU = line[:-2].decode()
    payload = "{"+Real_Time_Data+","+NLLFU+"}"
    mqtt_client.publish('Store/Raspi',payload, qos=1)
    time.sleep(1)
 
