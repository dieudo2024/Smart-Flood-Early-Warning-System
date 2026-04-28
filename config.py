import os

# AWS general configuration
AWS_PORT = 8883
AWS_HOST = 'key'

AWS_ROOT_CA = os.path.expanduser('~/certs/aws_root.pem')
AWS_CLIENT_CERT = os.path.expanduser('~/certs/aws_client.crt')
AWS_PRIVATE_KEY = os.path.expanduser('~/certs/aws_private.key')

################## Subscribe / Publish client #################
CLIENT_ID = 'fromPi'
TOPIC = 'iot/flood_monitor/DRS/data'
OFFLINE_QUEUE_SIZE = -1
DRAINING_FREQ = 2
CONN_DISCONN_TIMEOUT = 10
MQTT_OPER_TIMEOUT = 5
