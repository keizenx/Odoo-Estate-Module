from datetime import timedelta
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    _order = "price desc"

    price = fields.Float(required=True)
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False
    )
    partner_id = fields.Many2one(
        'res.partner',
        string="Partner",
        required=True
    )
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True
    )
    property_type_id = fields.Many2one(
        'estate.property.type',
        related='property_id.property_type_id',
        store=True
    )
    salesperson_id = fields.Many2one(
        "res.users", 
        string="Salesperson",
        related="property_id.user_id", 
        store=True
    )

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)',
         'The offer price must be strictly positive.'),
    ]

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        """Compute the deadline date based on creation date and validity period."""
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date.date() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        """Calculate validity period based on deadline date."""
        for record in self:
            base_date = record.create_date or fields.Date.today()
            record.validity = (record.date_deadline - base_date).days

    def action_accept(self):
        """Accept the current offer and update related property status."""
        for record in self:
            if record.property_id.state == 'sold':
                raise UserError(
                    "Cannot accept an offer for a sold property."
                )
            # Refuse all other offers
            record.property_id.offer_ids.filtered(lambda o: o.id != record.id).write({'status': 'refused'})
            record.status = 'accepted'
            record.property_id.write({
                'selling_price': record.price,
                'state': 'offer_accepted'
            })
        return True

    def action_refuse(self):
        """Mark the current offer as refused."""
        for record in self:
            record.status = 'refused'
        return True

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = self.env['estate.property'].browse(vals['property_id'])
            if property_id.state == 'sold':
                raise UserError("Cannot create offer for sold properties")
            if property_id.state == 'cancelled':
                raise UserError("Cannot create offer for cancelled properties")
        return super().create(vals_list)