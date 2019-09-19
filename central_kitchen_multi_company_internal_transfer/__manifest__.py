# -*- coding: utf-8 -*-

{
    'name': 'Central Kitchen MultiCompany Internal Transfer',
    'summary': """Central Kitchen MultiCompany Internal Transfer""",
    'version': '1.0',
    'description': """Create internal transfer between company”:""",
    'author': 'HashMicro / Kuashal Patel',
    'company': 'HashMicro ERP Solutions',
    'website': 'www.hashmicro.com',
    'category': 'Inventory',
    'depends': ['stock', 'purchase', 'multicompany_sales_purchase', 'central_kitchen'],
    'license': 'AGPL-3',
    'data': [
        'views/purchase_views.xml'
    ],
    'installable': True,
    'auto_install': False,

}
