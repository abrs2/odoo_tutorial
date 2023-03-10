from odoo import fields, models

class PurchaseOrderLine(models.Model):

    _inherit = "purchase.order.line"

    po_ac_audit_confirmation_status = fields.Selection(related="order_id.ac_audit_confirmation_status", store=True, string="Estatus de confirmación de disponibilidad de auditoría", readonly=True)
    po_coordinator_id = fields.Many2one(related="order_id.coordinator_id", store=True, string="Coordinador", readonly=True)