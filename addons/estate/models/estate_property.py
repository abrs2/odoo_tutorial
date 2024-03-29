
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import models,fields,api
from odoo.exceptions import UserError, ValidationError

def dateInThreeMonths():
    now= date.today()
    dateAfter = now+ relativedelta(months=3)
    year = dateAfter.strftime("%Y")
    month = dateAfter.month
    day = dateAfter.strftime("%d")

    fecha=year+'-'+str(month)+'-'+day

    return fecha
    

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "CRM Estate Property"

    _sql_constraints = [('check_expected_price','CHECK(expected_price > 0)','The expected price must be greater than 0'),
                        ('check_property_selling_price','CHECK(selling_price >= 0)','The property selling price must be greater than or equal to 0')]

    name = fields.Char(string='Property Name',default="Unknown",required=True,translate=True)
    tag_ids = fields.Many2many("estate.property.tag",string="Property Tags")
    property_type_id = fields.Many2one("estate.property.type",string="Property Type")
    description =fields.Text('Description')
    postcode = fields.Char('Postcode',required=True)
    date_availability = fields.Date('Available From',default=dateInThreeMonths(),copy=False)
    expected_price = fields.Float('Expected Price',required=True)
    selling_price = fields.Float('Selling Price',readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    total_area = fields.Integer("Total Area(sqm)",compute="_compute_area",readonly=True)
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north','North'), ('south','South'), ('east','East'),('west', 'West')],
        help="Garden Orientation is used to indicate where the garden is", default= 'please choose one',
        )    
    active= fields.Boolean('Active',default=True) 
    state = fields.Selection(
        string='Status',
        selection=[('new','New'),('offer received','Offer Received'), ('offer accepted','Offer Accepted'),
        ('sold','Sold'), ('canceled','Canceled')],
        copy=False,required=True,default='new',
    )

    salesMan = fields.Many2one("res.users",string="Salesman",default=lambda self: self.env.user)
    buyer = fields.Many2one("res.partner",string="Buyer",copy=False)

    offer_ids = fields.One2many("estate.property.offer","property_id")

    best_price= fields.Float("Best Price",compute="_compute_best_price",readonly=True)

    @api.depends("living_area","garden_area")
    def _compute_area(_self):
        for rec in _self:
            rec.total_area = rec.garden_area+rec.living_area

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            best_price=0
            for offer in record.offer_ids:
                if offer.price>best_price:
                    best_price= offer.price
            
            record.best_price = best_price
    
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'

            return {"warning":{
            'title':("Warning"),
            'message':("Ha cambiado el area y orientacion del jardin")}}

        else:
            self.garden_area = 0
            self.garden_orientation = ''

    def action_do_sold(self):
        allow = False

        if not self.state == 'canceled':
            self.state = 'sold'
            allow=True

        if not allow:

            raise UserError("You are not allowed to set a canceled property as sold")

        return True

    def action_do_cancel(self):
        
        allow = False

        if not self.state == 'sold':
            self.state = 'canceled'
            allow=True

        if not allow:
            
            raise UserError("You are not allowed to set a sold property as canceled")

        return True

    """
    @api.constrains('expected_price')
    def _check_expected_price(self):

        for record in self:
            if record.expected_price <1:
                raise ValidationError("Expected price cannot be zero or a negative number")

    @api.constrains('selling_price')
    def _check_selling_price(self):

        for record in self:
            if record.expected_price <1:
                raise ValidationError("Expected price cannot be zero or a negative number")

    
    """
            

