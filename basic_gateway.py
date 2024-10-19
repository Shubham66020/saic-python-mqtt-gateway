import paho.mqtt.client as mqtt
import random
import time

# MQTT Broker settings
BROKER_ADDRESS = "test.mosquitto.org"
BROKER_PORT = 1883
TOPIC = "iot/sensor/temperature"

# Simulating a sensor that generates random temperature values
def simulate_sensor_data():
    return round(random.uniform(20.0, 30.0), 2)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code {rc}")

# The callback for when a PUBLISH message is sent to the server.
def on_publish(client, userdata, mid):
    print(f"Data published successfully. Message ID: {mid}")

# Create an MQTT client instance
client = mqtt.Client()

# Assign the on_connect and on_publish callbacks
client.on_connect = on_connect
client.on_publish = on_publish

# Connect to the MQTT broker
client.connect(BROKER_ADDRESS, BROKER_PORT, 60)

# Start the network loop
client.loop_start()

# Simulate sensor data and publish it to the MQTT broker
try:
    while True:
        temperature = simulate_sensor_data()
        print(f"Sensor temperature: {temperature}°C")
        
        # Publish the sensor data to the topic
        client.publish(TOPIC, payload=temperature, qos=0, retain=False)
        
        # Wait before sending the next value
        time.sleep(5)

except KeyboardInterrupt:
    print("Gateway shutting down...")
finally:
    # Stop the network loop and disconnect from the broker
    client.loop_stop()
    client.disconnect()
