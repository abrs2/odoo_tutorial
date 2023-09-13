from odoo import http
from odoo.http import request,json
import logging

_logger = logging.getLogger(__name__)

class WebForm(http.Controller):
    
    @http.route('/submit_web_form', type='http', website=True, auth="public")
    def submit_form(self, **kw):
         return request.render('custom.form_template', {})
    
    @http.route('/create/web_form_record', type='http', website=True, auth="public", Methods=['POST'])
    def create_form(self, **kw):
        data = json.loads(kw['data_line_ids'])
        val = [(0, 0, line) for line in data]
        values = {
            'name': kw['name'],
            'data_line_ids': val,
        }
        form_id = request.env['web.form.test'].sudo().create(values)
        return request.render('custom.form_template', {})




    
