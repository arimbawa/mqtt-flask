import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt

app = Flask(__name__)
socketio = SocketIO(app)

MQTT_BROKER = 'broker.hivemq.com'
MQTT_PORT = 1883
MQTT_TOPIC = 'UNRAM'

# MQTT setup
def on_connect(client, userdata, flags, rc):
    print("Connected to broker with code", rc)
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(f"Received on {msg.topic}: {message}")
    socketio.emit('mqtt_message', {'data': message})

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/publish', methods=['POST'])
def publish():
    message = request.form.get('message')
    if message:
        mqtt_client.publish(MQTT_TOPIC, message)
        print(f"Published: {message}")
    return redirect(url_for('index'))

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000, debug=True)
