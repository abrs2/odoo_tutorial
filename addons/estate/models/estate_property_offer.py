from odoo import models,fields,api
from logging import getLogger
from dateutil.relativedelta import relativedelta
from datetime import *
import dateutil

import logging

_logger = logging.getLogger(__name__)

class EstatePropertyOffer(models.Model): 
    _name = 'estate.property.offer'

    price = fields.Float("Price")
    validity = fields.Integer("Validity(days)",default=7)
    date_deadline = fields.Date("Date Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)
    status = fields.Selection(string="Status",selection=[('accepted','Accepted'),('refused','Refused')],copy=False,)
    partner_id = fields.Many2one("res.partner",string="Partner")
    property_id = fields.Many2one("estate.property",string="Property")

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                date_1= (datetime.strptime(record.create_date.strftime('%Y-%m-%d'),'%Y-%m-%d')+relativedelta(days =+ record.validity))
                record.date_deadline = date_1
            else:
                now = datetime.now() # current date and time
                date_1= (datetime.strptime(now.strftime('%Y-%m-%d'),'%Y-%m-%d')+relativedelta(days =+ record.validity))
                record.date_deadline = date_1

    
    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                created=dateutil.parser.parse(str(record.create_date)).date()
                delta= record.date_deadline-created
                record.validity= delta.days
                _logger.error("--------------------------- validity -> "+str(record.validity)+" delta from create_date -> "+str(delta)+"-------------------------------------")
    
    '''        else:
                now = date.today# current date and time 
                delta= record.date_deadline-now
                record.validity= delta.days
                
                _logger.error("--------------------------- validity -> "+str(record.validity)+" delta from now -> "+str(delta)+"-------------------------------------")


    @api.onchange('invoice_payed')
    def _check_change(self):
        if self.invoice_payed:
            date_1= (datetime.strptime(self.invoice_payed, '%Y-%m-%d')+relativedelta(days =+ 42))

            self.pay_date =date_1
'''
    
