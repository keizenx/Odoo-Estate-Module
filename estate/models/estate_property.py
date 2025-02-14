"""
This module defines the estate property model.
"""

from odoo import models, fields, api, exceptions
from odoo.tools import float_compare, float_is_zero
from odoo.exceptions import UserError, ValidationError

class EstateProperty(models.Model):
    """
    This class represents an estate property.
    """
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(required=True)
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    postcode = fields.Char()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ])
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')
    ], required=True, default='new')
    best_price = fields.Float(compute="_compute_best_price")
    user_id = fields.Many2one(
        'res.users', 
        string='Salesperson', 
        default=lambda self: self.env.user,
        tracking=True
    )

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 
         'Expected price must be strictly positive'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 
         'Selling price must be positive'),
    ]

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for prop in self:
            prop.best_price = max(prop.offer_ids.mapped('price') or [0.0])

    def action_sold(self):
        if self.state == 'cancelled':
            raise UserError("Cancelled properties cannot be sold.")
        self.state = 'sold'
        return True

    def action_cancel(self):
        if self.state == 'sold':
            raise UserError("Sold properties cannot be cancelled.")
        self.state = 'cancelled'
        return True

    @api.constrains('selling_price', 'expected_price')
    def _check_price_difference(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2):
                if float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) < 0:
                    raise ValidationError("Selling price cannot be lower than 90% of expected price.")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'offer_ids' in vals:
                vals['state'] = 'offer_received'
        return super().create(vals_list)

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_cancelled(self):
        if any(property.state not in ['new', 'cancelled'] for property in self):
            raise UserError("Only new and cancelled properties can be deleted.")

    @api.model
    def _valid_field_parameter(self, field, name):
        return name == 'tracking' or super()._valid_field_parameter(field, name)

# Ensure the file ends with a newline 