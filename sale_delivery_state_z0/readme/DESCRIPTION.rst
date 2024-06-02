This odoo module add delivery state on the sale order.

Delivery state is computed based on ``qty_delivered`` field on sale order lines.

This is usefull for other modules to provide the state of delivery.
The state of the sale order can be forced to fully delivered in case
some quantities were cancelled by the customer and you consider you have
nothing more to deliver.

Sale order lines can have products or services, as long as the field ``qty_delivered``
is set, it will trigger the computation of delivery state.

This module also works with delivery.carrier fees that are added as a
sale order line. Those line are special as they will never be considered delivered.
Delivery fees lines are ignored in the computation of the delivery state.

This module is the backport from Odoo 12.0. Its name is *sale_delivery_state_zo* to
avoid conflict with OCA module *sale_delivery_state* that is avaialbel starting from
Odoo 12.0. You should rename this module into *sale_delivery_state*.
