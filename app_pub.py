from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt

app = Flask(__name__)
socketio = SocketIO(app)

MQTT_BROKER = 'broker.hivemq.com'
MQTT_PORT = 1883
MQTT_TOPIC = 'UNRAM'

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(f"Received: {message}")
    socketio.emit('mqtt_message', {'data': message})

# MQTT Setup
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.loop_start()

@app.route('/pub')
def index():
    return render_template('index_pub.html')

@app.route('/publish', methods=['POST'])
def publish():
    message = request.form.get('message')
    if message:
        mqtt_client.publish(MQTT_TOPIC, message)
        print(f"Published: {message}")
    return redirect(url_for('index'))

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)
