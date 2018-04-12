# coding: utf-8
#   @author Giacom Grasso <giacomo.grasso.82@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _
from odoo.exceptions import Warning as UserError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    installation_id = fields.Many2one(
        string="Installation",
        comodel_name="installation.main")
    officer_id = fields.Many2one(
        string="Admin./Rappr.",
        comodel_name="res.partner",
        domain=[('officer', "!=", False)])

    @api.multi
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        res = super(SaleOrder, self).onchange_partner_id()
        self.officer_id = self.partner_id.officer_id.id

        return res

    @api.multi
    def action_confirm(self):
        edits = super(SaleOrder, self).action_confirm()
        for item in self:
            if item.state in ['sale', 'done']:
                for line in item.order_line:
                    if line.product_id.create_task:
                        line.create_task()

        return edits  # super(SaleOrder, self).write(vals)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    def create_task(self):
        task = self.env['project.task']
        name = "[{}] {} ".format(
            self.order_id.name.encode("utf-8"),
            self.name.encode("utf-8"),
            )
        project = self.env['project.project'].search([
            ('analytic_account_id', '=', self.order_id.project_id.id)])
        if not project:
            raise UserError(_("Please define a project for the order"))

        if not project.user_id:
            raise UserError(_("Please define a project manager for the project"))

        new_task_data = ({
            'name': name,
            'project_id': project.id,
            'partner_id': self.order_id.partner_id.id,
            'user_id': project.user_id.id,
            'plain_description': self.name,
            'sale_line_id': self.id,
            'officer_id': self.order_id.officer_id.id,
            'installation_id': self.order_id.installation_id.id,
        })

        task.create(new_task_data)