=======================================================================================================
|icon| Sale Order Line Quantity Policy/Politiche di quantità delle righe d'ordine di vendita 10.0.0.1.5
=======================================================================================================

**Declare sale order line delivered or invoiced by product policy**

.. |icon| image:: https://raw.githubusercontent.com/zeroincombenze/l10n-italy-supplemental/10.0/sale_order_line_qty_policy/static/description/icon.png


.. contents::



Overview | Panoramica
=====================

|en| Odoo evaluates the status of a sale order line from quantities only: a line is
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


|it| Odoo valuta lo stato di una riga d'ordine solo in base alle quantità: una riga
è fatturata quando la quantità fatturata raggiunge quella ordinata (o quella
consegnata, in base alla politica di fatturazione del prodotto). Esistono però
casi ricorrenti in cui questa regola lascia l'ordine aperto all'infinito.

Questo modulo permette di dichiarare una riga d'ordine consegnata o fatturata,
manualmente oppure tramite una politica dichiarata sul prodotto.

Sul prodotto sono disponibili due politiche:

* **Dichiara automaticamente fatturato**: ogni riga di questo prodotto è
  considerata interamente fatturata alla conferma dell'ordine. Questa funzione
  è richiesta dai moduli che gestiscono prodotti di tipo imposta, come il
  contributo ambientale (CONAI), il cui importo viene rivalutato a livello di
  fattura: la quantità fatturata non coinciderà mai con quella ordinata e
  l'ordine resterebbe in uno stato incompleto o errato.

* **Soglia di consegna**: per alcuni prodotti non è possibile consegnare
  l'esatta quantità ordinata. Quando lo scostamento fra quantità ordinata e
  consegnata rientra nella percentuale dichiarata, la riga è considerata
  interamente consegnata e l'ordine si chiude non appena la quantità
  consegnata è stata fatturata. La soglia può essere dichiarata sul prodotto
  oppure, una sola volta per un'intera famiglia di prodotti, sulla categoria
  prodotto.

La quantità consegnata non viene mai alterata dal modulo: al cliente è sempre
fatturata la quantità realmente consegnata.


|thumbnail|

.. |thumbnail| image:: https://raw.githubusercontent.com/zeroincombenze/l10n-italy-supplemental/10.0/sale_order_line_qty_policy/static/description/


Configuration | Configurazione
------------------------------

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



Usage | Utilizzo
----------------

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



Getting started | Primi passi
=============================

|Try Me|


Prerequisites | Prerequisiti
----------------------------

* python 2.7+ (best 2.7.5+)
* postgresql 9.2+ (best 9.5)

::

    cd $HOME
    # Follow statements activate deployment, installation and upgrade tools
    cd $HOME
    [[ ! -d ./tools ]] && git clone https://github.com/zeroincombenze/tools.git
    cd ./tools
    ./install_tools.sh -pUT
    source $HOME/devel/activate_tools



Installation | Installazione
----------------------------

+---------------------------------+------------------------------------------+
| |en|                            | |it|                                     |
+---------------------------------+------------------------------------------+
| These instructions are just an  | Istruzioni di esempio valide solo per    |
| example; use on Linux CentOS 7+ | distribuzioni Linux CentOS 7+,           |
| Ubuntu 14+ and Debian 8+        | Ubuntu 14+ e Debian 8+                   |
|                                 |                                          |
| Installation is built with:     | L'installazione è costruita con:         |
+---------------------------------+------------------------------------------+
| `Zeroincombenze Tools <https://zeroincombenze-tools.readthedocs.io/>`__ |
+---------------------------------+------------------------------------------+
| Suggested deployment is:        | Posizione suggerita per l'installazione: |
+---------------------------------+------------------------------------------+
| $HOME/10.0 |
+----------------------------------------------------------------------------+

::

    # Odoo repository installation; OCB repository must be installed
    deploy_odoo clone -r l10n-italy-supplemental -b 10.0 -G zero -p $HOME/10.0
    # Upgrade virtual environment
    vem amend $HOME/10.0/venv_odoo



Upgrade | Aggiornamento
-----------------------

::

    deploy_odoo update -r l10n-italy-supplemental -b 10.0 -G zero -p $HOME/10.0
    vem amend $HOME/10.0/venv_odoo
    # Adjust following statements as per your system
    sudo systemctl restart odoo



Support | Supporto
------------------

|Zeroincombenze| This module is supported by the `SHS-AV s.r.l. <https://www.zeroincombenze.it/>`__



Get involved | Ci mettiamo in gioco
===================================

Bug reports are welcome! You can use the issue tracker to report bugs,
and/or submit pull requests on `GitHub Issues
<https://github.com/zeroincombenze/l10n-italy-supplemental/issues>`_.

In case of trouble, please check there if your issue has already been reported.



Proposals for enhancement
-------------------------

|en| If you have a proposal to change this module, you may want to send an email to <cc@shs-av.com> for initial feedback.
An Enhancement Proposal may be submitted if your idea gains ground.

|it| Se hai proposte per migliorare questo modulo, puoi inviare una mail a <cc@shs-av.com> per un iniziale contatto.



ChangeLog History | Cronologia modifiche
----------------------------------------

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



Credits | Ringraziamenti
========================

Copyright
---------

Odoo is a trademark of `Odoo S.A. <https://www.odoo.com/>`__ (formerly OpenERP)


Authors | Autori
----------------

* `SHS-AV s.r.l. <https://www.zeroincombenze.it>`__



Contributors | Partecipanti
---------------------------

* `Antonio M. Vigliotti <info@shs-av.com>`__



Maintainer | Manutenzione
-------------------------

* `Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>`__



----------------

|en| **zeroincombenze®** is a trademark of `SHS-AV s.r.l. <https://www.shs-av.com/>`__
which distributes and promotes ready-to-use **Odoo** on own cloud infrastructure.
`Zeroincombenze® distribution of Odoo <https://www.zeroincombenze.it/>`__
is mainly designed to cover Italian law and markeplace.

|it| **zeroincombenze®** è un marchio registrato da `SHS-AV s.r.l. <https://www.shs-av.com/>`__
che distribuisce e promuove **Odoo** pronto all'uso sulla propria infrastuttura.
La distribuzione `Zeroincombenze® <https://www.zeroincombenze.it/>`__ è progettata per le esigenze del mercato italiano.


|
|

This module is part of l10n-italy-supplemental project.

Last Update / Ultimo aggiornamento: 2026-09-02

.. |Maturity| image:: https://img.shields.io/badge/maturity-Alfa-black.png
    :target: https://odoo-community.org/page/development-status
    :alt: 
.. |license gpl| image:: https://img.shields.io/badge/licence-LGPL--3-7379c3.svg
    :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
    :alt: License: LGPL-3
.. |license opl| image:: https://img.shields.io/badge/licence-OPL-7379c3.svg
    :target: https://www.odoo.com/documentation/user/14.0/legal/licenses/licenses.html
    :alt: License: OPL
.. |Try Me| image:: https://www.zeroincombenze.it/wp-content/uploads/ci-ct/prd/button-try-it-10.svg
    :target: https://erp10.zeroincombenze.it
    :alt: Try Me
.. |Zeroincombenze| image:: https://avatars0.githubusercontent.com/u/6972555?s=460&v=4
   :target: https://www.zeroincombenze.it/
   :alt: Zeroincombenze
.. |en| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/flags/en_US.png
   :target: https://www.facebook.com/Zeroincombenze-Software-gestionale-online-249494305219415/
.. |it| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/flags/it_IT.png
   :target: https://www.facebook.com/Zeroincombenze-Software-gestionale-online-249494305219415/
.. |check| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/check.png
.. |no_check| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/no_check.png
.. |menu| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/menu.png
.. |right_do| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/right_do.png
.. |exclamation| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/exclamation.png
.. |warning| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/warning.png
.. |same| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/same.png
.. |late| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/late.png
.. |halt| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/halt.png
.. |info| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/awesome/info.png
.. |xml_schema| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/certificates/iso/icons/xml-schema.png
   :target: https://github.com/zeroincombenze/grymb/blob/master/certificates/iso/scope/xml-schema.md
.. |DesktopTelematico| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/certificates/ade/icons/DesktopTelematico.png
   :target: https://github.com/zeroincombenze/grymb/blob/master/certificates/ade/scope/Desktoptelematico.md
.. |FatturaPA| image:: https://raw.githubusercontent.com/zeroincombenze/grymb/master/certificates/ade/icons/fatturapa.png
   :target: https://github.com/zeroincombenze/grymb/blob/master/certificates/ade/scope/fatturapa.md
