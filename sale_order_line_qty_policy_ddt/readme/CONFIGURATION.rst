No configuration is needed: the module bridges two modules which are already
configured.

The policies declared on the product by `sale_order_line_qty_policy` are the
very same ones used here:

* **Auto declare invoiced**: every delivery note line of this product is
  considered invoiced, exactly as every sale order line of it is.

The **Delivered threshold (%)** is not evaluated on the delivery note: the
threshold compares the ordered quantity with the delivered one and the
delivery note *is* the delivery, so it carries the delivered quantity only.
The threshold keeps being evaluated on the sale order line.
