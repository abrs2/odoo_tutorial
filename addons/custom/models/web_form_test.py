from odoo import models, fields

class WebFormTest(models.Model):
	_name = 'web.form.test'
	_description = 'Web Form Test'

	name = fields.Char(string='Name', required=True)
	data_line_ids = fields.One2many('data.line', 'form_id', 'Data Lines')