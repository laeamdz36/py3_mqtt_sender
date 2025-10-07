# MQTT python 3 Sender - InfluxDB 2 line protocol

Aplication for development and test the influxdb 2 line protocol configurations to send
to a MQTT broker that and to be captuired by telegraf and ingest in a influxDB data storage.

### Libraries

- paho.mqtt
- dotenv

### .env file variables to be set

- BROKER_MQTT = _The ip address_
- BROKER_PORT = _Port of the broker server_
- BROKER_USER = _User to access to the MQTT broker_
- BROKER_PWD = _"Password for the MQTT user broker_