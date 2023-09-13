from odoo import models, fields

class DataLine(models.Model):
	_name = 'data.line'
	_description = 'Data Lines'

	code = fields.Char('Product Code', required=True)
	cost = fields.Float('Cost', required=True)
	form_id = fields.Many2one('web.form.test', 'Form Id', ondelete='cascade', required=True)
