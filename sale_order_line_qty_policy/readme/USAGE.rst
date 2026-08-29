On a confirmed sale order, the manager can flag every line with:

* **Declared delivered**: the line is considered fully delivered whatever the
  delivered quantity is. The delivered quantity is not altered, so the customer
  is still invoiced for what has been really delivered.

* **Declared invoiced**: the line is considered fully invoiced and it is no
  more selected when an invoice is created from the order.

Both flags are available from the order line list and from the
*Sales Order Lines* list, where the filters *Fully Delivered*,
*Declared Delivered* and *Declared Invoiced* are added.

The same result can be obtained from code with the methods
``action_declare_delivered()``, ``action_undeclare_delivered()``,
``action_declare_invoiced()`` and ``action_undeclare_invoiced()`` of
``sale.order.line``.

At order level, ``force_delivery_state`` is kept aligned with the lines: it
is set when every relevant line is delivered and cleared when it is not. The
field is shared with ``sale_delivery_state_z0``, which shows the order as
delivered, and neither module depends on the other one. As soon as a user
writes the flag by hand, ``force_delivery_state_manual`` is set and the policy
stops managing that order.

When the order is reset to draft, the delivered quantity of the stockable
lines is written back from the stock moves still linked to them. Standard Odoo
detaches every procurement from its line at that moment, so the delivered
quantity is reset; without this, a line would keep forever the quantity of the
last delivery, even when the goods were returned. Services keep the quantity
entered by hand.

The technical field ``line_delivered`` is stored and computed: it is true when
the line reached the ordered quantity, or the deviation is within the product
threshold, or the line was declared delivered.
