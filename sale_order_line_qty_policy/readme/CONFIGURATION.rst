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
