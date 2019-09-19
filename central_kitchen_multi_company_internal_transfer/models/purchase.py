# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.model
    def default_get(self, fields):
        res = super(PurchaseOrder, self).default_get(fields)
        if self._context.get('show_central_kitchen'):
            res.update({'central_kitchen': True})
        return res

    central_kitchen = fields.Boolean('Central Kitchen')

    @api.onchange('central_kitchen')
    def onchange_is_internal_company(self):
        domain = {}
        for rec in self:
            if rec.central_kitchen:
                partner_ids = [c.partner_id.id for c in self.env.user.company_ids]
                partner_ids = partner_ids + self.env['res.partner'].search([('supplier', '=', True)]).ids
                domain = {'partner_id': [(
                    'id', 'in', partner_ids)]}
            else:
                domain = {'customer_id': [(
                    'company_id', '=', self.env.user.company_id.id)]}
        return {'domain': domain}

    @api.multi
    def button_confirm(self):
        result = super(PurchaseOrder, self).button_confirm()
        print("self.related_so",self.related_so)
        if len(self.related_so):
            try:
                self.related_so.action_confirm()
                for pick in self.related_so.picking_ids:
                    location_id = self.picking_ids and self.picking_ids[0].location_dest_id
                    itls = []
                    for line in self.order_line:
                        itl = {
                            'name': line.product_id.name,
                            'product_id': line.product_id.id,
                            'price_unit': line.price_unit,
                            'product_uom_qty': line.product_qty,
                        }
                        itls.append(self.env['internal.transfer.line'].create(itl).id)
                    internal_transfer = {
                        'partner_id': pick.partner_id.id,
                        'source_loc_id': pick.location_id.id,
                        'dest_loc_id': location_id.id,
                        'product_line_ids': [(6, 0 , itls)],
                        'picking_ids': [(6, 0, self.related_so.picking_ids.ids + self.picking_ids.ids)],
                        'picking_type_outgoing_id': pick.picking_type_id.id,
                        'picking_type_incoming_id': self.picking_ids and self.picking_ids[0].picking_type_id.id,
                        'state': 'confirm',
                    }
                    transfer_id = self.env['internal.transfer'].create(internal_transfer)
                    pick.write({'transfer_out': True, 'transfer_id': transfer_id.id})
                    self.picking_ids[0].write({'transfer_id': transfer_id.id, 'transfer_in': True})
            except Exception as e:
                raise UserError(_(e))
        return result
