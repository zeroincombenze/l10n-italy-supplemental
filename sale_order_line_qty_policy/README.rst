================================
Sale Order Line Quantity Policy
================================

Odoo evaluates the status of a sale order line from quantities only: a line is
invoiced when the invoiced quantity reaches the ordered one (or the delivered
one, depending on the invoicing policy of the product). There are however
common cases where this rule keeps an order open forever.

This module makes it possible to declare a sale order line delivered or
invoiced, either manually or by a policy declared on the product.

Two policies are available on the product:

* **Auto declare invoiced**: every line of this product is considered fully
  invoiced as soon as the order is confirmed. This is required by modules
  managing tax products, i.e. the environmental contribution (CONAI), whose
  amount is evaluated again at invoice level: the invoiced quantity will never
  match the ordered one, so the order would be left in an incomplete or wrong
  status.

* **Delivered threshold**: for some products it is not possible to deliver the
  exact ordered quantity. When the deviation between ordered and delivered
  quantity is within the declared percentage, the line is considered fully
  delivered and the order is closed as soon as the delivered quantity has been
  invoiced. The threshold can be declared on the product or, once for a whole
  family of products, on the product category.

The delivered quantity is never altered by this module: the customer is always
invoiced for the quantity really delivered.


Configuration
=============

On the product form, tab *Invoicing*, section *Quantity Policy*:

* **Delivered threshold (%)**: maximum accepted deviation, as a percentage of
  the ordered quantity, between ordered and delivered quantity. The deviation
  is evaluated on its absolute value, so both under and over delivery are
  covered. Leave 0 to inherit the threshold of the product category.

The same **Delivered threshold (%)** is available on the product category form,
so it can be declared once for a whole family of products. The threshold of the
product wins; the one of the category is used only when the product does not
declare its own. Leave both to 0 to disable the policy.

* **Auto declare invoiced**: check it to declare invoiced every sale order line
  of this product.

Both fields are declared on the product template, so the policy applies to all
the variants of the product.


Usage
=====

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


Credits
=======

Authors
-------

* SHS-AV s.r.l. <https://www.zeroincombenze.it>

Contributors
------------

* Antonio M. Vigliotti <info@shs-av.com>
