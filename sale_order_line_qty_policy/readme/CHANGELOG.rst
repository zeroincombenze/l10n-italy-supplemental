10.0.0.1.5 (2026-09-01)
~~~~~~~~~~~~~~~~~~~~~~~

* [NEW] Italian translation

10.0.0.1.4 (2026-08-29)
~~~~~~~~~~~~~~~~~~~~~~~

* [REM] Migration script removed: the orders confirmed before the installation
  are evaluated when one of their lines changes, they are no more evaluated in
  bulk during the upgrade

10.0.0.1.3 (2026-08-29)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] The migration script evaluates the orders by batches: on a production
  database the previous version loaded every confirmed order in one shot and
  died of MemoryError, making the whole upgrade fail
* [FIX] force_delivery_state_auto replaced by force_delivery_state_manual: the
  flag now belongs to the quantity policy unless a user wrote it, so an unknown
  value can no more leave an order stuck in delivered state

10.0.0.1.2 (2026-08-29)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Reset to draft writes back the real delivered quantity of stockable
  lines: standard Odoo detaches the procurements from the line and leaves
  qty_delivered with the value of the last delivery, even after a return

10.0.0.1.1 (2026-08-29)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Shared field force_delivery_state on sale.order, automatically set
  when every relevant line is delivered, so sale_delivery_state_z0 shows the
  order as done without any dependency between the two modules

10.0.0.1.0 (2026-08-29)
~~~~~~~~~~~~~~~~~~~~~~~

* [NEW] Initial implementation
* [NEW] Product fields delivered_threshold and auto_line_invoiced
* [NEW] Product category field delivered_threshold, used as default
* [NEW] Sale order line flags force_delivered and force_invoiced
