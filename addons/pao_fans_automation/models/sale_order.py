from odoo import fields, models, api
import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    global_gap_appications_ids = fields.One2many(
        "pao.global.gap.application", "sale_order_id", string='GOLBALGAP Applications associated to this sale')
    # Only count globalgap applications, but in the future, as more schemes are added, will consider them
    global_gap_appications_count = fields.Integer(
        'Application Count', compute="_compute_applications_count")

    @api.depends('global_gap_appications_ids')
    def _compute_applications_count(self):
        for order in self:
            if order.global_gap_appications_ids:
                order.global_gap_appications_count = len(
                    order.global_gap_appications_ids)
            else:
                order.global_gap_appications_count = 0
        
    def action_view_globalgap(self):
        self.ensure_one()

        list_view_id = self.env.ref('pao_fans_automation.view_application_tree').id
        form_view_id = self.env.ref('pao_fans_automation.view_application_form').id

        action = {'type': 'ir.actions.act_window_close'}
        
        action = self.env["ir.actions.actions"]._for_xml_id("pao_fans_automation.action_view_globalgap")
        action['context'] = {}  # erase default context to avoid default filter
        if len(self.global_gap_appications_ids) > 1:  # cross project kanban task
            _logger.error("---------------"+str(self.global_gap_appications_ids.ids)+"-------------")
            action['views'] = [[list_view_id, 'tree'], [form_view_id, 'form']]
            action['domain'] = [('id', 'in', self.global_gap_appications_ids.ids)]
        elif len(self.global_gap_appications_ids) == 1:  # single task -> form view
            action['views'] = [(form_view_id, 'form')]
            action['res_id'] = self.global_gap_appications_ids.id
        # filter on the task of the current SO
        action.setdefault('context', {})
        action['context'].update({'default_sale_order_id': self.id})
        return action
    

    def action_create_global_gap_application(self):
        
        """
        Add global gap id record for particular sale order
        """

        global_gap_appication_id = self.env['pao.global.gap.application'].create({
            'sale_order_id': self.id,
            'ggn': 'Test',
            'plNumber': 'Test PL',
            'coordinator_id': self.env.uid
            })
    
    def action_send_email_fans(self):
        
        _logger.error(
          "------------------Metodo action send email se ejecuta -----------------------")
      
        '''
        This function opens a window to compose an email, with the emai template message loaded by default
        '''

        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = \
                ir_model_data.get_object_reference('sale_order', 'sale_order_email_fans_template')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = {
            'default_model': 'sale.order',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
        }

        return {
            'name': 'Envío de FANS',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }
        
        
