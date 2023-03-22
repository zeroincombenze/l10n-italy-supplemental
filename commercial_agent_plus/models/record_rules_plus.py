# -*- coding: utf-8 -*-
from xml import dom
from odoo import api, fields, models, _, tools
from odoo.exceptions import ValidationError, AccessError
from odoo.osv import expression

agent_group = 'commercial_agent_plus.commercial_agent_plus_agent_group'
agent_manager = 'commercial_agent_plus.commercial_agent_plus_manager_group'
agent_all = 'commercial_agent_plus.commercial_agent_plus_all_group'
agent_admin = 'commercial_agent_plus.commercial_agent_plus_agent_admin_group'


class BaseModelExtend(models.AbstractModel):
    _inherit = 'base'
    
    """
    Private function for additional rules
    """
    
    @api.model
    def _check_if_agent(self):
        if self.env.user.has_group(agent_group) and \
        not self.env.user.has_group(agent_all):
            return True
        return False
    
    @api.model
    def _get_agents_params(self):
        """
        Return list of allowed agents_ids for the current user
        """
        agents = [self.env.user.id]
        if self.env.user.has_group(agent_manager):
            agents += self.env.user.commercial_agent_employee_ids.ids
        return agents


class CommercialAgentPlusResPartnerRules(models.Model):
    _inherit = "res.partner"
    
    """
    Override base methods:
    * Agent:
        - if user has agent_group he can search/read/write/unlink 
          only own contacts
    * Manager:
        - if user has agent_manager group he can search/read/write/unlink 
          own contacts and all contacts from his agent employees
    * Agent All:
        - if user has agent_all group in addition to agent_group or 
          agent_manager group -> Standard Odoo Record Rules
    """
    
    @api.model
    def _define_agents_domain(self, original_domain):
        if self._check_if_agent():
            agents = self._get_agents_params()
            dd = expression.OR([
                [('commercial_agent_ids', 'in', agents)],
                [('user_ids', 'in', agents)],
                # [('parent_id.commercial_agent_ids', 'in', agents)]
            ])
            domain = expression.AND([
                dd,
                original_domain]
            )
            return domain
        return False

    def _agent_access_denied(self):
        """
        check if current agent user can access to datas
        if True he can't access
        """
        self.ensure_one()
        agents = self._get_agents_params()
        if set(agents).isdisjoint(self.commercial_agent_ids.ids) and \
        set(agents).isdisjoint(self.user_ids.ids) and \
        set(agents).isdisjoint(self.parent_id.commercial_agent_ids.ids):
            return True
        return False
    
    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        domain = self._define_agents_domain(args)
        if domain:
            args = domain

        res = super(CommercialAgentPlusResPartnerRules, self).search(
            args,
            offset=offset,
            limit=limit,
            order=order,
            count=count
        )

        return res

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        domain = self._define_agents_domain(args)
        if domain:
            args = domain

        return super(CommercialAgentPlusResPartnerRules, self).name_search(
            name=name,
            args=args,
            operator=operator,
            limit=limit
        )

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        args = self._define_agents_domain(domain)
        if args:
            domain = args

        return super(CommercialAgentPlusResPartnerRules, self).read_group(
            domain=domain,
            fields=fields,
            groupby=groupby,
            offset=offset,
            limit=limit,
            orderby=orderby,
            lazy=lazy
        )
    
    def read(self, fields=None, load='_classic_read'):
        result = super(CommercialAgentPlusResPartnerRules, self).read(
            fields=fields,
            load=load
        ) 
        new_result = []
        
        if self._check_if_agent():
            # if user is agent and he can't access to res.partner
            # clear all the fields
            for res in result:
                par = self.browse(res['id'])
                if par._agent_access_denied():
                    id = res['id']
                    res = {
                        x:False if not isinstance(res[x], list) else [] \
                        for x in res if x != 'id'
                    }
                    res['id'] = id
                new_result.append(res)
            result = new_result            
        return result

    def write(self, vals):
        if self._check_if_agent():
            for res in self:
                if res._agent_access_denied():
                    description = self.env['ir.model']._get(self._name).name
                    raise AccessError(
                        _("""
The requested operation can not be 
completed due to security restrictions.
Document type: %(document_kind)s (%(document_model)s) [%(document_id)s]
Operation: %(operation)s
User: %(user)s""") % {
                        'document_model': self._name,
                        'document_kind': description or self._name,
                        'operation': 'write',
                        'user': self._uid,
                        'document_id': res.id
                    })
        return super(CommercialAgentPlusResPartnerRules, self).write(vals)
    
    def unlink(self):
        if self._check_if_agent():
            for res in self:
                if res._agent_access_denied():
                    description = self.env['ir.model']._get(self._name).name
                    raise AccessError(
                        _("""
The requested operation can not be 
completed due to security restrictions.
Document type: %(document_kind)s (%(document_model)s) [%(document_id)s]
Operation: %(operation)s
User: %(user)s""") % {
                        'document_model': self._name,
                        'document_kind': description or self._name,
                        'operation': 'write',
                        'user': self._uid,
                        'document_id': res.id
                    })
        return super(CommercialAgentPlusResPartnerRules, self).unlink()


class CommercialAgentPlusMenu(models.Model):
    _inherit = "ir.ui.menu"
    
    @api.model
    @tools.ormcache('frozenset(self.env.user.groups_id.ids)', 'debug')
    def _visible_menu_ids(self, debug=False):
        """
        Override:
        * Agent:
            - if user has agent_group he can view only agents menu
        * Manager:
            - if user has agent_manager group he can view only agents menu
        * Agent All:
            - if user has agent_all group in addition to agent_group or 
            agent_manager group -> Standard Odoo Menu views
        """
        menus = super(CommercialAgentPlusMenu, self)._visible_menu_ids(debug=debug)
        
        if self._check_if_agent():
            menulist = self.browse(list(menus))
            agent_group_obj = self.env.ref(agent_group)
            visible = [
                m.id for m in menulist if agent_group_obj.id in m.groups_id.ids
            ]
            return set(visible)

        return menus
    
class CommercialAgentPlusIrView(models.Model):
    _inherit="ir.ui.view"
    
    def read_combined(self, fields=None):
        vals = super(CommercialAgentPlusIrView, self).read_combined(
            fields=fields
        )
        if self._check_if_agent():
            agent_browse = self.env.ref(agent_group)
            manager_browse = self.env.ref(agent_manager)
            view = self.search([
                ('model', '=', self.model),
                ('type', '=', self.type),
                ('mode', '=', 'primary'),
                ('groups_id', 'in', [agent_browse.id, manager_browse.id]),
                ('id', '!=', self.id)
            ])
            if view:
                return view[0].read_combined()
        return vals