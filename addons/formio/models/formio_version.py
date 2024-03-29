# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import api, fields, models


class Version(models.Model):
    _name = 'formio.version'
    _description = 'formio.js Version'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence DESC'

    name = fields.Char(
        "Name", required=True, tracking=True,
        help="""formio.js release/version.""")
    active = fields.Boolean(default=True)
    sequence = fields.Integer()
    description = fields.Text("Description")
    translations = fields.Many2many('formio.translation', string='Translations')
    assets = fields.One2many('formio.version.asset', 'version_id', string='Assets (js, css)', domain=[('type', 'in', ['css', 'js'])])
    css_assets = fields.One2many(
        'formio.version.asset', 'version_id', domain=[('type', '=', 'css')], copy=True,
        string='CSS Assets')
    js_assets = fields.One2many(
        'formio.version.asset', 'version_id', domain=[('type', '=', 'js')], copy=True,
        string='Javascript Assets')
    license_assets = fields.One2many(
        'formio.version.asset', 'version_id',  domain=[('type', '=', 'license')], copy=True,
        string='License Assets')

    def unlink(self):
        self.assets.unlink()
        domain = [('formio_version_id', 'in', self.ids)]
        self.env['formio.version.github.tag'].search(domain).write({'state': 'available'})
        return super(Version, self).unlink()

    @api.model
    def create(self, vals):
        res = super(Version, self).create(vals)
        self._update_versions_sequence()
        return res

    def write(self, vals):
        res = super(Version, self).write(vals)
        if 'name' in vals:
            self._update_versions_sequence()
        return res

    @api.model
    def _update_versions_sequence(self):
        versions = self.search([])
        names = sorted(versions.mapped('name'))
        seq = 0
        for name in names:
            seq += 1
            version = versions.filtered(lambda r: r.name == name)[0]
            version.sequence = seq
