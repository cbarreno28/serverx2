# -*- coding:utf-8 -*-

import threading
import logging
import random
import time
from odoo import models, fields, api, SUPERUSER_ID, _
from odoo.exceptions import ValidationError, UserError
import paho.mqtt.client as paho

_logger = logging.getLogger(__name__)

STATUS = [('pending', 'Pending'), ('send', 'Send'), ('received', 'Received'), ('resend', 'Resend')]


class MessagePlots(models.Model):
    _name = 'message.plots'
    _description = 'Message plots received from X2'

    raw_frame = fields.Char('Raw Frame')
    root_address = fields.Char('Root Address')
    x2_id = fields.Integer('X2 ID')
    timestamp = fields.Datetime('Timestamp')
    status = fields.Selection(STATUS, 'State', default='pending')
    url = fields.Char('URL')
    count = fields.Integer('Counter', default=0)

    @api.multi
    def change_resend(self):
        self.status = 'resend'
        self.count = self.count + 1

    @api.multi
    def resend_messages(self):
        messages = self.env['message.plots'].search([('status', '=', 'resend')])
        if messages:
            mq_client = paho.Client("ClienteX2%s" % random.randint(0, 1000000))
            mq_client.username_pw_set(username="biofeeder", password="BiofeederMQTT")
            broker = 'xb4cdf95-internet-facing-a67c98d9ae4b13a0.elb.us-east-1.amazonaws.com'
            mq_client.connect(broker)
            for message in messages:
                mq_client.publish("server/x2/%s" % message.root_address, message.raw_frame, 1)
                message.change_resend()
            mq_client.disconnect()
