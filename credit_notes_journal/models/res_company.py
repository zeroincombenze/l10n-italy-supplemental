# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResCompany(models.Model):
    _inherit = 'res.company'

    enable_credit_note_registrations = fields.Boolean(string='Abilita registri per Note di Credito')
