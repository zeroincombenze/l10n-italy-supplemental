# -*- coding: utf-8 -*-
# Copyright 2018 Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from osv import osv, fields


class IrSaveTable(osv.Model):
    _name = 'ir.save.table'

    _columns = {
        'name': fields.char('Table',
                            size=64,
                            required=True,
                            translate=True),
        'active': fields.boolean('Active'),
        'model_id': fields.many2one(
            'ir.model', 'Table Name'),
        'use_id': fields.boolean('Use id'),
        'field_id': fields.many2one(
            'ir.model.fields', 'Field Record',
            domain="[('model_id', '=', model_id)]",
            translate=False),
        'operator': fields.char('Op',
                                size=16,
                                required=True,
                                translate=False),
        'value': fields.char('Record',
                             required=True,
                             translate=False),
    }

    _defaults = {
        'active': True,
        'use_id': True,
        'operator': 'in',
    }

    def on_change_model(self, cr, uid, ids, model_id, context=None):
        #                            on_change="on_change_model(model_id)"/>
        model = self.pool.get('ir.model')
        res = {}
        res['model_id'] = model_id
        res['name'] = model.browse(cr, uid, model_id).name
        return res
