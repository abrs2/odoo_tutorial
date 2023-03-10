from odoo import models, fields, api
from datetime import *
class AuditorAuditsProgress(models.Model):

    _name = 'auditor.audits.progress'
    _description = "Auditor Audits Progress"

    auditor_id = fields.Many2one(
        string="Auditor",
        comodel_name='res.partner',
        ondelete='cascade',
        required=True,
        index=True,
        domain = [('ado_is_auditor','=',True)],
    )
    start_date = fields.Date(string="Season Start Date", default=datetime.strptime("2022-09-01", '%Y-%m-%d').date(),store=True)
    end_date = fields.Date(string="Season End Date", default=datetime.strptime("2023-08-31", '%Y-%m-%d').date(),store=True)
    audits_number = fields.Integer('Audits Number', readonly=True, compute="_get_audits_number", store= True)
    audits_target = fields.Integer('Target', readonly=True, related='auditor_id.paa_audit_quantity')
    progress_bar = fields.Integer('Progress', readonly=True, compute="_compute_progress_bar", store=True)


    @api.depends("auditor_id","start_date","end_date")
    def _get_audits_number(self):
        counter = 0
        for rec in self:
            domain = [('date_order', '>', rec.start_date),('date_order', '<', rec.end_date),('partner_id', '=', rec.auditor_id.id),('state','!=','cancel'),('state','!=','draft'),('state','!=','sent'),('state','!=','to approve')]
            purchaseordeline = self.env['purchase.order'].search(domain).order_line
            for r in purchaseordeline:
                qty = r.product_qty
                for p in r.product_id:
                    for c in p.categ_id:
                        if c.paa_schem_id:
                            counter+=qty
                                
        rec.audits_number=counter

    @api.depends("auditor_id","audits_target","start_date","end_date")
    def _compute_progress_bar(self):
        
        for u in self:
            if u.audits_number and u.audits_target:
                if not (u.audits_number==0 or u.audits_target==0):
                    audits_number = 0
                    #audits_number = (int) (u._get_audits_number/u.audits_target)*100     
                    domain = [('date_order', '>', u.start_date),('date_order', '<', u.end_date),('partner_id', '=', u.auditor_id.id),('state','!=','cancel'),('state','!=','draft'),('state','!=','sent'),('state','!=','to approve')]
                    purchaseordeline = self.env['purchase.order'].search(domain).order_line
                    for r in purchaseordeline:
                        qty = r.product_qty
                        for p in r.product_id:
                            for c in p.categ_id:
                                if c.paa_schem_id:
                                    audits_number+=qty
                                    
                    #progress = (int) (audits_number/u.audits_target)*100
                    progress = audits_number/u.audits_target
                    u.progress_bar= (int) (progress*100)
                else:
                    u.progress_bar = 0
            else:
                u.progress_bar = 0
