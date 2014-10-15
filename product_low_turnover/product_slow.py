import openerp.addons.decimal_precision as dp
from osv import osv, fields
from tools.translate import _

class product_low_turnover(osv.osv_memory):
    _name = 'product.low.turnover'
    _order = 'rate desc'

    _columns = {
               'product_id': fields.many2one('product.product','Product'),
               'qty_available': fields.float('Quantity'),
               'categ_id': fields.many2one('product.category', 'Category'),
               'product_brand_id': fields.many2one('product.brand', 'Brand'),
               'list_price': fields.float('Price', digits_compute=dp.get_precision('Product Price')),
               'uid': fields.many2one('res.users', 'User'),
               'rate':  fields.float("Rate", digits_compute=dp.get_precision('Discount')),
    }
    
product_low_turnover()
