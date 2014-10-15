from openerp.osv import fields, osv
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from openerp import tools
from openerp.tools.translate import _


class res_company(osv.osv):
    _inherit = "res.company"
    
    def _get_schedule_range(self, cr, uid, ids, context=None):
        company_obj = self.pool.get("res.company")
        company_id = company_obj._company_default_get(cr, uid, 'product_eventful_report', context=context)
        shedule = company_obj.browse(cr, uid, company_id).schedule_range
        date = (datetime.today() - relativedelta(days=shedule)).strftime(tools.DEFAULT_SERVER_DATE_FORMAT)
        return date
    
res_company()

class product_eventful_report(osv.osv_memory):
    _name = "product.eventful.report"
    
    _columns = {
        'date_from': fields.date('Start Date'),
        'date_to': fields.date("End Date"),
    }
    _defaults = {
        'date_from' : lambda self, cr, uid, c: self.pool.get('res.company')._get_schedule_range(cr, uid, 'product_eventful_report', context=c),
        'date_to': fields.date.context_today,
        }
    
        
    def product_report_open_window(self, cr, uid, ids, context=None):
        
        product_obj = self.pool.get('product.product')
        move_obj = self.pool.get('stock.move')
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')

        if context is None:
            context = {}
            
        data = self.read(cr, uid, ids, [], context=context)[0]
        
        date_from = data.get('date_from', False)  
        date_to = data.get('date_to', False) 
         
        result = mod_obj.get_object_reference(cr, uid, 'product_not_eventful', 'action_product_not_eventful')
        id = result and result[1] or False
        result = act_obj.read(cr, uid, [id], context=context)[0]
        result['name'] = _('Product Without Movement Between %s and %s') % (date_from, date_to)
        
        report_ids = self.pool.get('product.not.eventful').search(cr, uid, [('uid','=',uid)])
        self.pool.get('product.not.eventful').unlink(cr, uid, report_ids)
     
        cr.execute("select distinct product_id \
            from stock_move sm inner join stock_picking sp on sp.id = sm.picking_id \
            where type in ('out','in') and sm.date between %s and %s", (date_from, date_to))
        moved = cr.dictfetchall()
        ids = product_obj.search(cr, uid, [], context=context)
        for product in product_obj.read(cr, uid, ids, ['qty_available','categ_id','product_brand_id','list_price'], context=context):
            if product['qty_available'] > 0  and product['id'] not in moved:
                self.pool.get('product.not.eventful').create(cr, uid, {'product_id':product['id'],
                                                                      'qty_available':product['qty_available'],
                                                                      'categ_id':product['categ_id'] and product['categ_id'][0] or '',
                                                                      'product_brand_id':product['product_brand_id'] and product['product_brand_id'][0] or '',
                                                                      'list_price':product['list_price'],
                                                                      'uid':uid})
    
        
        
        
        
        return result

product_eventful_report()
