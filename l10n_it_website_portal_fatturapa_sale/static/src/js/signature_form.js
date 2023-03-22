odoo.define('l10n_it_website_portal_fatturapa_sale.signature_form', function (require) {
    "use strict";

    var FatturapaSalePortal = require('l10n_it_website_portal_fatturapa_sale.portal');
    var SignatureForm = require('portal.signature_form').SignatureForm;

    SignatureForm.include({
        submitSign: function (ev) {
            ev.preventDefault();
            var self = this;
            var super_event = this._super;
            var self_args = arguments;
            return FatturapaSalePortal.check_e_inv_data(self, "input[name='electronic_invoice_subjected_signature']", super_event, self_args);
        },
    });
});
