import time
import logging
import random
import paho.mqtt.client as paho
import odoo


_logger = logging.getLogger(__name__)


def start_mqtt(broker, dbname=None):
    r = random.randint(0, 1000000)
    mqtt_client = paho.Client("serverx2" + str(r))
    mqtt_client.username_pw_set(username="biofeeder", password="BiofeederMQTT")
    mqtt_client.connect(broker)
    time.sleep(5)
    # Creamos la subscripcion
    _logger.info("Creating subscription...")
    with odoo.api.Environment.manage():
        with odoo.registry(dbname).cursor() as new_cr:
            env = odoo.api.Environment(new_cr, odoo.SUPERUSER_ID, {})
            broker = env['broker.mqtt'].search([], limit=1)
            if broker:
                _logger.info("Subcribiendo...")
                mqtt_client.on_connect = broker.on_connect
                mqtt_client.on_disconnect = broker.on_disconnect
                mqtt_client.on_message = broker.on_message
                mqtt_client.loop_forever()  # start loop to process received messages
