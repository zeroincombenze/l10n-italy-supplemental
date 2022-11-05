====================================
Convert Sale Order to Purchase Order
====================================

Installation
============

* `Install <https://odoo-development.readthedocs.io/en/latest/odoo/usage/install-module.html>`__ this module in a usual way

Configuration
=============

* User must have access to create/write Purchase Order in order to convert to Purchase Order.
* Go to Sales settings via under `Configuration` >> `Settings`.
* Set Default State for created purchase_orders.
* Check `Allow Convert **state name**` field if you want allow to convert in current state.

Usage
=====

* Open menu ``Sales >> Quotations/Sale Order >> Choose SO``.
* If so in allowed state, there will be button ``Convert to Purchase Order``.
