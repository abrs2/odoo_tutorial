from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'

    _sql_constraints = [('check_unique_name','UNIQUE(name)','The property tag name must be UNIQUE')]

    name = fields.Char("Name", required=True, translate=True)