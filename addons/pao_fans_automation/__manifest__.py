# -*- coding: utf-8 -*-
{
    'name':'PAO Fans Automation',
    'version':'1.0',
    'author':'Abrahan Barrios',
    'category':'',
    'website':'https://paomx.com',
    'depends':['sale','base','portal','website','servicereferralagreement',
    ],
    'data':[
        #security
        'security/ir.model.access.csv',
        #data
        'data/email_template.xml',
        #demo
        #reports
        #views
        'views/aplications_menus.xml',
        'views/global_gap_application_views.xml',
        'views/website_form.xml',
        'views/templates.xml',
        'views/sale_order_views.xml',
        'views/cursojavascript.xml',

    ],
    'application':'True',     
    
}