from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class SnippetControllers(http.Controller):

    @http.route('/get_products', type="json", auth="public", website=True)
    def get_products(self):

        products = http.request.env['product.template'].search([], limit=10)
        p=[]

        for product in products:
            news = {
                "name":product.name,
                "list_price": product.list_price
            }
            p.append(news)

        
        return p





    
