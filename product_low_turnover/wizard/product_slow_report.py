from openerp.osv import fields, osv
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from openerp import tools
import openerp.addons.decimal_precision as dp


class res_company(osv.osv):
    _inherit = "res.company"
    
    def _get_schedule_range(self, cr, uid, ids, context=None):
        company_obj = self.pool.get("res.company")
        company_id = company_obj._company_default_get(cr, uid, 'product_turnover_report', context=context)
        shedule = company_obj.browse(cr, uid, company_id).schedule_range
        date = (datetime.today() - relativedelta(days=shedule)).strftime(tools.DEFAULT_SERVER_DATE_FORMAT)
        return date
    
res_company()

class product_turnover_report(osv.osv_memory):
    _name = "product.turnover.report"
    
    _columns = {
        'date_from': fields.date('Start Date'),
        'date_to': fields.date("End Date"),
        'rate':  fields.float("Rate", digits_compute=dp.get_precision('Discount')),
    }
    _defaults = {
        'date_from' : lambda self, cr, uid, c: self.pool.get('res.company')._get_schedule_range(cr, uid, 'product_turnover_report', context=c),
        'date_to': fields.date.context_today,
        'rate':30,
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
        rate = data.get('rate', False)
         
        result = mod_obj.get_object_reference(cr, uid, 'product_low_turnover', 'action_product_low_turnover')
        id = result and result[1] or False
        result = act_obj.read(cr, uid, [id], context=context)[0]
        result['name'] = _('Rotation Low Product with %s %% Between %s and %s') % (rate, date_from, date_to)
        
        report_ids = self.pool.get('product.low.turnover').search(cr, uid, [('uid','=',uid)])
        self.pool.get('product.low.turnover').unlink(cr, uid, report_ids)
     
        cr.execute("select distinct product_id ,SUM(product_qty) as sum\
            from stock_move sm inner join stock_picking sp on sp.id = sm.picking_id \
            where type ='out' and sm.date between %s and %s group by product_id", (date_from, date_to))
        moved = cr.dictfetchall()
        ids = product_obj.search(cr, uid, [], context=context)
        for product in product_obj.read(cr, uid, ids, ['qty_available','categ_id','product_brand_id','list_price'], context=context):
            for move in moved : 
                if product['id'] == move['product_id']:
                    if product['qty_available'] > 0   and  ((move['sum']/product['qty_available']) * 100) <= rate:
                        self.pool.get('product.low.turnover').create(cr, uid, {'product_id':product['id'],
                                                                      'qty_available':product['qty_available'],
                                                                      'categ_id':product['categ_id'] and product['categ_id'][0] or '',
                                                                      'product_brand_id':product['product_brand_id'] and product['product_brand_id'][0] or '',
                                                                      'list_price':product['list_price'],
                                                                      'uid':uid,
                                                                      'rate':((move['sum']/product['qty_available']) * 100)})
                                                                      

        
        
        
        
        return result

product_turnover_report()
