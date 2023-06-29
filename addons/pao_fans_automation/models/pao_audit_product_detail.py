from odoo import fields,models,api

class PaoAuditProductDetail(models.Model):

    _name = "pao.audit.product.detail"
    _description = "PAO Audit Product Detail"
    _rec_name = 'name'

    name = fields.Char("Name", required=True)
