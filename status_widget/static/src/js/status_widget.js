odoo.define('status_widget', function (require) {
    "use strict";
    var core = require('web.core');
    var data = require('web.data');
    var common = require('web.form_common');
    var Model = require('web.DataModel');
    var utils = require('web.utils');
    var form_widgets = require('web.form_widgets');

    var FieldSelection = common.AbstractField.extend(common. ReinitializeFieldMixin,{
        template: 'FieldSelection',
        events: {
            'change': 'store_dom_value',
        },
        init: function(field_manager, node) {
            this._super(field_manager, node);
            this.set("value", false);
            this.set("values", []);
            this.records_orderer = new utils.DropMisordered();
            this.field_manager.on("view_content_has_changed", this, function() {
                var domain = new data.CompoundDomain(this.build_domain()).eval();
                if (!_.isEqual(domain, this.get("domain"))) {
                    this.set("domain", domain);
                };
            });
        },
        initialize_field: function() {
            common.ReinitializeFieldMixin.initialize_field.call(this);
            this.on("change:domain", this, this.query_values);
            this.set("domain", new data.CompoundDomain(this.build_domain()).eval());
            this.on("change:values", this, this.render_value);
        },
        query_values: function() {
            var self = this;
            var def;
            if (this.field.type === "many2one") {
                var model = new Model(this.field.relation);
                def = model.call("name_search", ['', this.get("domain")], {"context": this.build_context()});
            } else {
                var values = _.reject(this.field.selection, function (v) { return v[0] === false && v[1] === ''; });
                def = $.when(values);
            };
            this.records_orderer.add(def).then(function(values) {
                if (! _.isEqual(values, self.get("values"))) {
                    self.set("values", values);
                };
            });
        },
        initialize_content: function() {
            // Flag indicating whether we're in an event chain containing a change
            // event on the select, in order to know what to do on keyup[RETURN]:
            // * If the user presses [RETURN] as part of changing the value of a
            //   selection, we should just let the value change and not let the
            //   event broadcast further (e.g. to validating the current state of
            //   the form in editable list view, which would lead to saving the
            //   current row or switching to the next one)
            // * If the user presses [RETURN] with a select closed (side-effect:
            //   also if the user opened the select and pressed [RETURN] without
            //   changing the selected value), takes the action as validating the row
            if(!this.get('effective_readonly')) {
                var ischanging = false;
                this.$el
                    .change(function () { ischanging = true; })
                    .click(function () { ischanging = false; })
                    .keyup(function (e) {
                        if (e.which !== 13 || !ischanging) { return; };
                        e.stopPropagation();
                        ischanging = false;
                    });
                this.setupFocus(this.$el);
            }
        },
        commit_value: function () {
            this.store_dom_value();
            return this._super();
        },
        store_dom_value: function () {
            if (!this.get('effective_readonly')) {
                this.internal_set_value(JSON.parse(this.$el.val()));
            };
        },
        set_value: function(value_) {
            value_ = value_ === null ? false : value_;
            value_ = value_ instanceof Array ? value_[0] : value_;
            this._super(value_);
        },
        render_value: function() {
            var values = this.get("values");
            values =  [[false, this.node.attrs.placeholder || '']].concat(values);
            var found = _.find(values, function(el) { return el[0] === this.get("value"); }, this);
            if (!found) {
                found = [this.get("value"), _t('Unknown')];
                values = [found].concat(values);
            };
            if (!this.get("effective_readonly")) {
                this.$el.empty();
                for(var i = 0 ; i < values.length ; i++) {
                    this.$el.append($('<option/>', {
                        value: JSON.stringify(values[i][0]),
                        html: values[i][1]
                    }));
                };
                this.$el.val(JSON.stringify(found[0]));
            } else {
                this.$el.text(found[1]);
            };
        },
        focus: function() {
            if (!this.get("effective_readonly")) {
                return this.$el.focus();
            };
            return false;
        },
    });

    form_widgets.FieldSelection = FieldSelection;

    var statusWidget = form_widgets.FieldSelection.extend({
        /**
         * @override
         */
        render_value: function () {
            this._super(this, arguments);

            if(this.$el[0].localName == 'span') {
                this.$el.parent().css("display","flex");
                this.$el.prepend('<img id="status" src="/status_widget/static/src/img/'+this.get('value')+'.png"/>');
            };
        },
    });

    core.form_widget_registry.add('status_widget', statusWidget);
});
