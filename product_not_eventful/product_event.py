import openerp.addons.decimal_precision as dp
from osv import osv, fields
from tools.translate import _


class product_not_eventful(osv.osv_memory):
    _name = 'product.not.eventful'

    _columns = {
               'product_id': fields.many2one('product.product','Product'),
               'qty_available': fields.float('Quantity'),
               'categ_id': fields.many2one('product.category', 'Category'),
               'product_brand_id': fields.many2one('product.brand', 'Brand'),
               'list_price': fields.float('Price', digits_compute=dp.get_precision('Product Price')),
               'uid': fields.many2one('res.users', 'User'),
    }
    
product_not_eventful()
