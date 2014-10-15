{
    'name' : 'Product Without Movement',
    'version' : '1.0',
    'author': 'ERP SYSTEMS',
    'website': '',    
    'summary': 'Product Without Movement',
    'description': """
    
Features:
==========

* Adds a menu item "Product Not Moved" which opens a wizard for user to select products not moved between two dates.
 
    """,
    'category': 'Sales Management',
    'sequence': 25,
    'website': 'http://www.e-erp-sys.com',
    'depends' : ['sale','purchase','product_report_menu'],
    'data' : [
              'wizard/product_non_eventual_view.xml',
              'product_event_view.xml',
              ],
    'test' : [],
    'auto_install': False,
    'application': True,
    'installable': True,
}

