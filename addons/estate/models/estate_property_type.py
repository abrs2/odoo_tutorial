from odoo import models,fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    _sql_constraints = [('check_unique_name','UNIQUE(name)','The property type name must be UNIQUE')]

    name = fields.Char(required=True)
