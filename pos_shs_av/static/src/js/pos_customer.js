openerp.pos_shs_av = function (instance) {
    var _t = instance.web._t;
    var QWeb = instance.web.qweb;

    instance.point_of_sale.ProductScreenWidget = instance.point_of_sale.ProductScreenWidget.extend({
        init: function() {
            this._super.apply(this, arguments);
        },
        start:function(){
            this._super.apply(this, arguments);
            orderView = new instance.point_of_sale.OrderWidget(this, {});
            pos = this.pos;
            selectedOrder = this.pos.get('selectedOrder');
            if ($('button.select-order').length == 1) {
                pos = this.pos;
                $("#customer_link").click(function() {
                    selectedOrder = pos.get('selectedOrder');
                    var self = this;
                    new instance.web.Model("res.partner").get_func("search_read")(domain=[['customer', '=', true]], fields=['id'], offset=0, limit=20).pipe(
                        function(result) {
                            initial_ids = _.map(result, function(x) {return x['id']});
                            var pop = new instance.web.form.SelectCreatePopup(this);
                            pop.select_element(
                                'res.partner',
                                {
                                    title: 'Select Customer',
                                    initial_ids: initial_ids,
                                    initial_view: 'search',
                                    disable_multiple_selection: true
                                }
                        );
                        pop.on("elements_selected", self, function(element_ids) {
                            var dataset = new instance.web.DataSetStatic(self, 'res.partner', {});
                            dataset.name_get(element_ids).done(function(data) {
                                selectedOrder.set_client(data[0][1]);
                                selectedOrder.set_client_id(data[0][0]);
                                selectedOrder.set_pricelist_val(data[0][0]);
                            });
                        });
                    });
                });
            }
        },
        close: function(){
            this._super();
            this.pos_widget.order_widget.set_numpad_state(null);
            this.pos_widget.payment_screen.set_numpad_state(null);
        }
    });
    
    instance.point_of_sale.Orderline = instance.point_of_sale.Orderline.extend({
        can_be_merged_with: function(orderline){
            if( this.get_product().get('id') !== orderline.get_product().get('id')){    //only orderline of the same product can be merged
                return false;
            }else if(this.get_product_type() !== orderline.get_product_type()){
                return false;
            }else if(this.get_discount() > 0){             // we don't merge discounted orderlines
                return false;
//            }else if(this.price !== orderline.price){
//                return false;
            }else{ 
                return true;
            }
        }
    });
    
    instance.point_of_sale.Order = instance.point_of_sale.Order.extend({
        initialize: function(attributes){
            Backbone.Model.prototype.initialize.apply(this, arguments);
            this.set({
                creationDate:   new Date(),
                orderLines:     new instance.point_of_sale.OrderlineCollection(),
                paymentLines:   new instance.point_of_sale.PaymentlineCollection(),
                name:           "Order " + this.generateUniqueId(),
                client:         null,
                client_id:      null,
                pricelist_val:  null,
            });
            this.pos =     attributes.pos; 
            this.selected_orderline = undefined;
            this.screen_data = {};  // see ScreenSelector
            this.receipt_type = 'receipt';  // 'receipt' || 'invoice'
            return this;
        },
        set_client_id: function(client_id) {
            this.set('client_id', client_id)
        },
        get_client_id: function(){
            return this.get('client_id');
        },
        get_client_name: function(){
            var client = this.get('client');
            return client ? client : "";
        },
        set_pricelist_val: function(client_id) {
            var self = this;
            if (client_id) {
                new instance.web.Model("res.partner").get_func("read")(parseInt(client_id), ['property_product_pricelist']).pipe(
                    function(result) {
                        self.set('pricelist_val', result.property_product_pricelist[0] || '');
                    }
                );
            }
        },
        get_pricelist: function() {
            return this.get('pricelist_val');
        },
        exportAsJSON: function() {
            var orderLines, paymentLines;
            orderLines = [];
            (this.get('orderLines')).each(_.bind( function(item) {
                return orderLines.push([0, 0, item.export_as_JSON()]);
            }, this));
            paymentLines = [];
            (this.get('paymentLines')).each(_.bind( function(item) {
                return paymentLines.push([0, 0, item.export_as_JSON()]);
            }, this));
            
            return {
                name: this.getName(),
                amount_paid: this.getPaidTotal(),
                amount_total: this.getTotalTaxIncluded(),
                amount_tax: this.getTax(),
                amount_return: this.getChange(),
                lines: orderLines,
                statement_ids: paymentLines,
                pos_session_id: this.pos.get('pos_session').id,
                partner_id: parseInt(this.get_client_id()) || "",
                user_id: this.pos.get('cashier') ? this.pos.get('cashier').id : this.pos.get('user').id,
            };
        },
        addProduct: function(product, options){
            options = options || {};
            var attr = product.toJSON();
            attr.pos = this.pos;
            attr.order = this;
            var line = new instance.point_of_sale.Orderline({}, {pos: this.pos, order: this, product: product});
            var partner_id = parseInt(this.get_client_id());
            var pricelist_id = parseInt(this.get_pricelist());
            var uom = null;
            
            if(options.quantity !== undefined){
                line.set_quantity(options.quantity);
            }
            if(options.price !== undefined){
                line.set_unit_price(options.price);
            }
            var last_orderline = this.getLastOrderline();
            if( last_orderline && last_orderline.can_be_merged_with(line) && options.merge !== false){
                last_orderline.merge(line);
                var qty = last_orderline.get_quantity();
                if (partner_id) {
                    if (pricelist_id) {
                        new instance.web.Model("product.pricelist").get_func('price_get')([pricelist_id], product.id, qty).pipe(
                            function(res){
                                if (res[pricelist_id]) {
                                    pricelist_value = parseFloat(res[pricelist_id].toFixed(2));
                                    if (pricelist_value) {
                                        last_orderline.set_unit_price(pricelist_value);
                                    }
                                }
                            }
                        );
                    }
                }
            } else {
                var pricelist_value = null;
                if (partner_id && pricelist_id) {
                    var self = this;
                    new instance.web.Model("product.template").get_func("read")(parseInt(product.id), ['uom_id']).pipe(
                        function(result) {
                            if (result && result.uom_id) {
                                uom = result.uom_id[0];
                            }
                        }
                    );
                    new instance.web.Model("product.pricelist").get_func('price_get')([pricelist_id], product.id, 1).pipe(
                        function(res){
                            if (res && res[pricelist_id]) {
                                pricelist_value = parseFloat(res[pricelist_id].toFixed(2));
                                if (pricelist_value) {
                                    line.set_unit_price(pricelist_value);
                                    self.get('orderLines').add(line);
                                    self.selectLine(self.getLastOrderline());
                                }
                                else {
                                    self.get('orderLines').add(line);
                                    self.selectLine(self.getLastOrderline());
                                }
                            }
                        }
                    );
                } else {
                    this.get('orderLines').add(line);
                }
            }
            this.selectLine(this.getLastOrderline());
        }
    });
    
    instance.point_of_sale.OrderWidget = instance.point_of_sale.OrderWidget.extend({
        set_value: function(val) {
            var order = this.pos.get('selectedOrder');
            if (order.get('orderLines').length !== 0) {
                var mode = this.numpadState.get('mode');
                if( mode === 'quantity'){
                    var partner_id = parseInt(order.get_client_id());
                    var pricelist_id = parseInt(order.get_pricelist());
                    if ((val != 'remove') && pricelist_id && order && order.getSelectedLine().get_product().id) {
                        var p_id = order.getSelectedLine().get_product().id;
                        if (! val) {
                            val = 1;
                        }
                        new instance.web.Model("product.pricelist").get_func('price_get')([pricelist_id], p_id, val).pipe(
                            function(res){
                                if (res[pricelist_id]) {
                                    pricelist_value = parseFloat(res[pricelist_id].toFixed(2));
                                    if (pricelist_value && order.getSelectedLine()) {
                                        order.getSelectedLine().set_quantity(val);
                                        order.getSelectedLine().set_unit_price(pricelist_value);
                                    }
                                }
                            }
                        );
                    } else {
                        order.getSelectedLine().set_quantity(val);
                    }
                }else if( mode === 'discount'){
                    order.getSelectedLine().set_discount(val);
                }else if( mode === 'price'){
                    order.getSelectedLine().set_unit_price(val);
                }
            } else {
                if (this.pos.get('selectedOrder')) {
                    this.pos.get('selectedOrder').destroy();
                    alert('Selected order has been cleared !');
                }
            }
        }
    });
}