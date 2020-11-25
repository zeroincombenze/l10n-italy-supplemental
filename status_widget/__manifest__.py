{
    'name': 'Status Widget',
    'version': '10.0.1.0.0',
    'author': "Mark Okolov",
    'description': '''
        Add new custom widget 'status_widget' that adding picture to selection field.\n

        Rules for adding pictures:\n
            * You must name the picture as selection value (f.e.: if value is 'done' that picture name should be 'done.png');\n
            * Add this picture to folder 'static/src/img/' in this module.\n
        Rules for activate this widget:\n
            * In xml file add 'widget="status_widget"' for field (f.e.: '<field name="test_selection" widget="status_widget"/>')\n
    ''',
    'license': '',
    'category': 'Widget',
    'depends': [
        'base',
        'web',
    ],
    'data': [
        'assets.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],
    'installable': True,
}
