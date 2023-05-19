from odoo import fields,models,api

class PaoGlobalGapApplication(models.Model):
    
    _name = "pao.global.gap.application"
    _description = "PAO Global Gap Application"
    _rec_name = 'plNumber'

    plNumber = fields.Char("PL-México",required=True,copy=False,help="Asigned by Primus Auditing Operations")
    ggn = fields.Char(string="GGN",required=True,help="Asigned by GLOBAL G.A.P.")
    version = fields.Selection(
        string='Version',
        selection=[('5.4-1','V5.4-1-GFS'), ('5.3','V5.3-GFS')],
        help="It refers to the Global Gap version on which the customer would like to get certified", default= '5.4-1',
        )
    