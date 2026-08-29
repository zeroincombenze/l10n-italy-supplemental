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
