{
    'name' : 'Rotation Low Product',
    'version' : '1.0',
    'author': 'ERP SYSTEMS',
    'website': '',    
    'summary': 'Rotation Low Product',
    'description': """
    
Features:
==========

* Adds a menu item "Product low moved" which opens a wizard for user to select low moved products  between two dates and less to the rate defined.
 
    """,
    'category': 'Sales Management',
    'sequence': 25,
    'website': 'http://www.e-erp-sys.com',
    'depends' : ['sale','purchase','product_report_menu'],
    'data' : [
              'product_slow_view.xml',
              'wizard/product_slow_report_view.xml',
              ],
    'test' : [],
    'auto_install': False,
    'application': True,
    'installable': True,
}

