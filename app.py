import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt

app = Flask(__name__)
socketio = SocketIO(app)

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")
    client.subscribe("UNRAM")

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print("MQTT Message:", message)
    socketio.emit('mqtt_message', {'data': message})

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect("broker.hivemq.com", 1883, 60)
mqtt_client.loop_start()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, debug=True)
