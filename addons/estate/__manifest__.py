{
    'name':'Real Estate',
    'depends':[
        'base'
    ], 
    'data':[

        #security
        'security/ir.model.access.csv',
        #data
        'views/dashboard_action.xml',
        #demo
        #reports
        #views
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/res_users_properties_views.xml',
        'views/estate_menus.xml',
    ],
    'qweb':[
        'static/src/dashboard.xml',
    ],
    'application':'True',                            
}