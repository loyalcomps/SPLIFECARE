from odoo.tools import float_is_zero
from odoo.exceptions import UserError
from odoo import fields, models, api, _


class ResCompany(models.Model):
    _inherit = "res.company"

    roundoff_account_id = fields.Many2one('account.account',string="Round Off Account")