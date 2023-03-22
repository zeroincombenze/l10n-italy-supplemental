odoo.define('commercial_agent_plus.agent_tour', function (require) {
    'use strict';
    var core = require('web.core');
    var tour = require('web_tour.tour');
    var _t = core._t;

    tour.register('Create_agent_tour', {
        url: "/web#action=base.action_res_users",
        rainbowMan: true,
        rainbowManMessage: _t("<b> Congratulations! </b> You've created your first agent!"),
        sequence: 1000,
    }, [ {
            trigger: ".o_list_button_add",
            content: _t("Create a user."),
            position: "bottom"
        },{
            trigger: ".o_field_char[name='login']",
            content: _t("Fill in all the previous mandatory fields and enter your username or email."),
            position: "bottom"
        },{
            trigger: ".o_form_label:contains('Agent')",
            content: _t("Remove all other roles and select Agent or Manager. When you are done click on the label above."),
            position: "bottom",
        },{
            trigger: _t(".o_form_label:contains('Agent Admin')"),
            content: _t("Select this field if you want the user to be an administrator Agents app (Can have access to all records of agents, customers, orders, commission orders, settlements and settings). When you are done click on the label above."),
            position: "top",
        }, {
            trigger: _t(".o_form_label:contains('Agent all')"),
            content: _t("Select this field if you want the agent to also acquire other roles and see the records as a common Odoo user. Otherwise the agent will only see the agent app and only the records linked to him. When you are done click on the label above."),
            position: "top",
        }, {
            trigger: ".o_form_button_save",
            content: _t("Save user."),
            position: "bottom",
        }, {
            trigger: ".o_cp_action_menus .o_dropdown .btn",
            ontent: _t("Open menu to change password."),
            position: "bottom",
        }, {
            trigger: ".o_menu_item .dropdown-item:contains('password')",
            content: _t("Click to change password"),
            position: "right",
        }, {
            trigger: ".o_field_char[name='new_passwd']",
            extra_trigger: ".modal-dialog",
            content: _t("Write password."),
            position: "bottom",
        }, {
            trigger: "button[name='change_password_button']",
            content: _t("Save password."),
            position: "bottom",
        }
    ]);
	
    tour.register('Configure_agent_tour', {
        url: "/web#action=commercial_agent_plus.commercial_agent_customers_action&view_type=kanban",
        rainbowMan: true,
        rainbowManMessage: _t("<b> Congratulations! </b> You've configured your first agent!"),
        sequence: 1001,
    },[
        {
            trigger: ".o_filter_menu",
            content: _t("Open filter menu."),
            position: "bottom"
        },
        {
            trigger: ".o_menu_item:contains('Agent')",
            content: _t("Filter by Agents."),
            position: "right"
        },
        {
            trigger: ".o_kanban_record:contains('Agent')",
            content: _t("Choose you first agent."),
            position: "bottom"
        },
        {
            trigger: ".o_form_button_edit",
            content: _t("Choose edit mode."),
            position: "bottom"
        },
        {
            trigger: ".o_notebook_headers .nav-item:contains('Agent')",
            content: _t("Open agent Tab."),
            position: "top"
        },
        {
            trigger: ".o_field_widget[name='commercial_agent_manager_id']",
            content: _t("If you want choose the manager of this agent."),
            position: "bottom"
        },
        {
            trigger: ".o_field_widget[name='commercial_agent_commission_type']",
            content: _t("Choose whether commissions are paid on invoices (invoiced) or payments (cashed)"),
            position: "bottom"
        },
        {
            trigger: ".o_field_widget[name='commercial_agent_area_ids']",
            content: _t("If you want, choose the areas of expertise."),
            position: "top"
        },
        {
            trigger: ".o_field_widget[name='commercial_agent_commission_ids']",
            content: _t("Configure commission lines. The order of calculation is: Product + Customer; Product; Product Category; Customer; Price list; Area; Default Product (configurable in the product form); Default Agent."),
            position: "top"
        },
        {
            trigger: ".o_form_button_save",
            content: _t("Save agent."),
            position: "bottom"
        }
    ]
    );
    tour.register('Configure_product_agent_tour', {
        url: "/web#action=commercial_agent_plus.commercial_agent_product_action&view_type=kanban",
        rainbowMan: true,
        rainbowManMessage: _t("<b> Congratulations! </b> You've configured your first product agent!"),
        sequence: 1002,
    }, [
        {
            trigger: ".o-kanban-button-new",
            content: _t("Create a product or choose one from the list."),
            position: "bottom"
        },
        {
            trigger: ".o_notebook_headers .nav-item:contains('ommiss')",
            content: _t("Open commission Tab."),
            position: "top"
        },
        {
            trigger: ".o_field_widget[name='commercial_agent_salable']",
            content: _t("Set to True if you want the product to be sold by agents."),
            position: "right"
        },
        {
            trigger: ".o_field_widget[name='commercial_agent_commission_free']",
            content: _t("Set to True if you want the product to be excluded from commissions."),
            position: "right"
        },
        {
            trigger: ".o_field_widget[name='product_commission_ids']",
            content: _t("Configure the default commissions for the product."),
            position: "top"
        }
    ]
    );
    tour.register('Configure_customer_agent_tour', {
        url: "/web#action=commercial_agent_plus.commercial_agent_customers_action&view_type=kanban",
        rainbowMan: true,
        rainbowManMessage: _t("<b> Congratulations! </b> You've configured your first customer agent!"),
        sequence: 1003,
    }, [
        {
            trigger: ".o-kanban-button-new",
            content: _t("Create a customer or choose one from the list."),
            position: "bottom"
        },
        {
            trigger: _t(".o_notebook_headers .nav-item:contains('Sales')"),
            content: _t("Open Sale & Purchase Tab."),
            position: "top"
        },
        {
            trigger: ".o_field_widget[name='commercial_agent_ids']",
            content: _t("Choose the agents of this customer."),
            position: "right"
        },
        {
            trigger: ".o_field_widget[name='commercial_agent_area_ids']",
            content: _t("If you want, choose the areas of expertise."),
            position: "top"
        }
    ]
    );
});