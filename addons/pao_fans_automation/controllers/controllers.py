# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json
from odoo.exceptions import ValidationError

class OdooControllers(http.Controller):
    @http.route(['/get_globalgap_audit_products'],type='json', auth='public', website=True)
    def get_globalgap_audit_products(self, **kw):
        audit_products = http.request.env['servicereferralagreement.auditproducts'].sudo().search([])

        p = []

        for product in audit_products:
            n = {
                "name":product.name,
                "id":product.id
            }
            
            p.append(n)

        p.sort(key=lambda x: x["name"])

        return p
    
    @http.route(['/get_globalgap_countries'],type='json', auth='public', website=True)
    def get_globalgap_countries(self, **kw):
        countries = http.request.env['res.country'].sudo().search([])

        c = []

        for country in countries:
            n = {
                "name":country.name,
                "id":country.id
            }
            
            c.append(n)

        c.sort(key=lambda x: x["name"])

        return c
    
    
    @http.route(['/get_globalgap_states'],type='json', auth='public', website=True)
    def get_globalgap_states(self, country_id):

        states = http.request.env['res.country.state'].sudo().search([('country_id','=',int(country_id))])
        #if country_id:
        #    raise ValidationError((str(country_id)))   
        s = []

        for state in states:
            n = {
                "name":state.name,
                "id":state.id
            }
            
            s.append(n)

        s.sort(key=lambda x: x["name"])
        
        return s
    
    @http.route(['/get_globalgap_cities'],type='json', auth='public', website=True)
    def get_globalgap_cities(self, state_id):

        states = http.request.env['res.city'].sudo().search([('state_id','=',int(state_id))])
        #if country_id:
        #    raise ValidationError((str(country_id)))   
        c = []

        for state in states:
            n = {
                "name":state.name,
                "id":state.id
            }
            
            c.append(n)

        c.sort(key=lambda x: x["name"])
        
        return c