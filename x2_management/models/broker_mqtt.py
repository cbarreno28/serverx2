# -*- coding:utf-8 -*-

import threading
import logging
import random
import time
from odoo import models, fields, api, SUPERUSER_ID, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime
import paho.mqtt.client as paho
from ..command.mqtt import start_mqtt

_logger = logging.getLogger(__name__)


class BrokerMQTT(models.Model):
    _name = 'broker.mqtt'

    name = fields.Char('Name')
    url = fields.Char('Url')

    def on_connect(self, client, userdata, flags, rc):
        client.subscribe("x2/#")
        _logger.info("Connected flags " + str(flags) + "result code " + str(rc) + str(self))

    def on_message(self, client, userdata, message):
        try:
            root_address = message.topic.split("/")[1]
        except IndexError:
            _logger.info("No se puede sacar el dispositivo en este topico %s" % message.topic)
            return
        _logger.info("Receiving packet from %s %s" % (message.topic, message.payload))
        try:
            message_id = self.env['message.plots'].create({'raw_frame': message.payload,
                                                           'x2_id': False,
                                                           'timestamp': datetime.now(),
                                                           'status': 'pending',
                                                           'root_address': root_address,
                                                           'url': False})
            _logger.info("Mensaje creado %s..." % message_id.id)
            self.env.cr.commit()
        except Exception as e:
            _logger.info("Error when creating message " + str(e))

    def on_disconnect(self, client, userdata, rc):
        _logger.info(f"Me desconecte del servidor MQTT, reconectando {rc}..")
        client.reconnect()
        client.subscribe("serverx2/#")
        time.sleep(5)

    @api.model
    def execute_mqtt_thread(self):
        try:
            broker = 'xb4cdf95-internet-facing-a67c98d9ae4b13a0.elb.us-east-1.amazonaws.com'
            th = threading.Thread(target=start_mqtt, args=(broker, self.env.cr.dbname))
            th.start()
        except:
            pass