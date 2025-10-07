import time
import os
import random as rd
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

status = None

# load credentials
load_dotenv()


def load_config() -> list[str]:
    """Load env file to get Broker keys"""

    address = os.getenv("BROKER_MQTT")
    port = os.getenv("BROKER_PORT")
    user = os.getenv("BROKER_USER")
    pwd = os.getenv("BROKER_PWD")
    if address is None or port is None:
        raise ValueError(
            "BROKER_MQTT and BROKER_PORT environment variables must be set")
    if user is None or pwd is None:
        raise ValueError(
            "BROKER_USER and BROKER_PWD environment variables must be set")
    return [address, port, user, pwd]


def create_client() -> mqtt.Client:
    """Connect to the MQTT Broker"""

    address, port, user, pwd = load_config()
    # client = mqtt.Client()
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.username_pw_set(user, pwd)
    try:
        client.connect(address, port=int(port))
    except Exception as e:
        print(f"Connection error to broker {e}")
        exit()
    return client


def dev_msg_influx(topic) -> dict:
    """Definition of the format to publish to InfluxDB"""
    value_1 = rd.randint(1, 30)
    value_2 = rd.randint(1, 100)
    measurement = "TEST01"
    location = "Dev_location"
    id_sensor = "366"
    payload_str = (
        f"{measurement},"
        f"location={location},id_sensor={id_sensor} "
        f"value_1={value_1}i,value_2={value_2}i")
    pyload_influx = {"payload": payload_str, "topic": topic}
    return pyload_influx


def pub_influx_payload(client: mqtt.Client, msg):
    """Publish to client mqtt a influx payload"""

    global status
    try:
        result = client.publish(msg["topic"], payload=msg["payload"])
        status = result[0]
        if status == 0:
            print(f"Message sent to topic: {msg["payload"][0]}")
        else:
            print(f"Failure to send to {msg["topic"]}")
        return status
    except Exception as e:
        print(f"Error {e}")
        return status


def main(client: mqtt.Client):
    """Main execution loop"""

    topic = "DEV"
    # load topics and msgs to publish
    message = dev_msg_influx(topic)
    pub_influx_payload(client, message)


if __name__ == "__main__":

    mqtt_client = create_client()
    while True:
        main(mqtt_client)
        if status != 0:
            print("Closing program")
            break
        time.sleep(3)
