from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class WebForm(http.Controller):

	@http.route('/submit_web_form', type='http', website=True, auth="public")
	def submit_form(self, **kw):
    		return request.render('web_form.form_template', {})





    
