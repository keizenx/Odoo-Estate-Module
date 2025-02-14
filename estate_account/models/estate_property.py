from odoo import models, Command
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        _logger.info("Starting action_sold in estate_account")
        try:
            res = super().action_sold()
            _logger.info("Super action_sold completed successfully")
        except Exception as e:
            _logger.error("Error in super action_sold: %s", str(e))
            raise UserError(f"Cannot sell property: {str(e)}")

        try:
            # Vérifier l'accès au module de comptabilité
            if not self.env['ir.module.module'].search([('name', '=', 'account'), ('state', '=', 'installed')]):
                _logger.warning("Account module not installed")
                return res

            # Chercher le journal
            journal = self.env['account.journal'].search([('type', '=', 'sale')], limit=1)
            if not journal:
                _logger.error("No sales journal found")
                raise UserError("No sales journal found. Please configure one.")

            for prop in self:
                # Vérifier l'offre acceptée
                accepted_offer = prop.offer_ids.filtered(lambda o: o.status == 'accepted')
                if not accepted_offer:
                    _logger.warning("No accepted offer found for property %s", prop.name)
                    continue

                _logger.info("Creating invoice for property %s", prop.name)
                invoice = self.env['account.move'].with_context(default_move_type='out_invoice').create({
                    'partner_id': accepted_offer.partner_id.id,
                    'move_type': 'out_invoice',
                    'journal_id': journal.id,
                    'invoice_line_ids': [
                        Command.create({
                            'name': f'Property: {prop.name}',
                            'quantity': 1.0,
                            'price_unit': prop.selling_price * 0.06,
                        }),
                        Command.create({
                            'name': 'Administrative fees',
                            'quantity': 1.0,
                            'price_unit': 100.0,
                        }),
                    ],
                })
                _logger.info("Invoice created successfully with id %s", invoice.id)

        except Exception as e:
            _logger.error("Error in estate_account action_sold: %s", str(e))
            raise UserError(f"Cannot create invoice: {str(e)}")

        return res 