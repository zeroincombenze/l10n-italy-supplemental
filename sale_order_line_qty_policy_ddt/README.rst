===================================================================================================================
|icon| Sale Order Line Quantity Policy - DdT/Politiche di quantità delle righe d'ordine di vendita - DdT 10.0.0.1.0
===================================================================================================================

**Bridge module: quantity policy applied to DdT based invoices**

.. |icon| image:: https://raw.githubusercontent.com/zeroincombenze/l10n-italy-supplemental/10.0/sale_order_line_qty_policy_ddt/static/description/icon.png


.. contents::



Overview | Panoramica
=====================

|en| `l10n_it_ddt` creates invoices from delivery notes (DdT) instead of from sale
orders, and it evaluates a delivery note from its lines only: the document is
declared invoiced when every one of its lines was turned into an invoice line
during one single run of the invoicing procedure.

`sale_order_line_qty_policy` makes it possible to declare a sale order line
invoiced without any invoice line at all, either by hand or by a policy
declared on the product, i.e. the environmental contribution (CONAI) whose
amount is evaluated again at invoice level.

Without this bridge module the two behaviours contradict each other: a
delivery note carrying a line the quantity policy declares invoiced can never
be closed. The invoicing procedure skips that line, so the invoice reference
of the delivery note is never written; the document keeps showing up as to be
invoiced and every further attempt to invoice it ends with *There is no
invoicable line*, which in the mass invoicing wizard takes down the invoicing
of every other delivery note of the period.

This module introduces on the delivery note line the same concepts the
quantity policy introduces on the sale order line, and it adds to the
delivery note the invoice status Odoo gives to a sale order.


|it| `l10n_it_ddt` crea le fatture dai documenti di trasporto (DdT) anziché dagli
ordini di vendita e valuta il DdT dalle sole righe: il documento è dichiarato
fatturato quando tutte le sue righe sono diventate righe di fattura in una
singola esecuzione della procedura di fatturazione.

`sale_order_line_qty_policy` permette di dichiarare fatturata una riga
d'ordine anche senza alcuna riga di fattura, manualmente oppure tramite una
politica dichiarata sul prodotto, come il contributo ambientale (CONAI) il cui
importo viene rivalutato a livello di fattura.

Senza questo modulo ponte i due comportamenti si contraddicono: un DdT che
contiene una riga dichiarata fatturata dalla politica di quantità non può mai
essere chiuso. La procedura di fatturazione salta quella riga, quindi il
riferimento alla fattura non viene mai scritto sul DdT; il documento continua
a risultare da fatturare e ogni ulteriore tentativo di fatturarlo termina con
*There is no invoicable line*, errore che nella procedura di fatturazione
massiva blocca la fatturazione di tutti gli altri DdT del periodo.

Questo modulo introduce sulla riga del DdT gli stessi concetti che la politica
di quantità introduce sulla riga d'ordine e aggiunge al DdT lo stato di
fatturazione che Odoo attribuisce all'ordine di vendita.


|thumbnail|

.. |thumbnail| image:: https://raw.githubusercontent.com/zeroincombenze/l10n-italy-supplemental/10.0/sale_order_line_qty_policy_ddt/static/description/


Configuration | Configurazione
------------------------------

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



Usage | Utilizzo
----------------

On a delivery note, the manager can flag every line with:

* **Declared invoiced**: the line is considered fully invoiced and it is no
  more selected when an invoice is created from the delivery note. Use it when
  the goods of that line must not be billed, i.e. a free replacement.

The same result can be obtained from code with the methods
``action_declare_invoiced()`` and ``action_undeclare_invoiced()`` of
``stock.picking.package.preparation.line``.

The technical field ``line_invoiced`` is stored and computed: it is true when
an invoice line was created from the delivery note line, or the line was
declared invoiced, or the product carries the *Auto declare invoiced* policy,
or the **sale order line was declared invoiced**. That last case is the point
of the bridge: a decision taken on the order is never contradicted by the
delivery note, which would otherwise bill the customer for what the order
declares already invoiced.

The declaration travels from the order to the delivery note and never the
other way round: a delivery note line is one of the several deliveries of an
order line, so it cannot decide for it. When the order has to be closed as
well, declare its own line invoiced: `sale_order_line_qty_policy` handles it.

At delivery note level, **Invoice status** carries the same three values Odoo
uses for a sale order:

* *Nothing to invoice*: the delivery note is not invoiceable yet, or its
  reason for transportation declares it is not to be invoiced;
* *To invoice*: at least one line has still to be invoiced;
* *Fully invoiced*: every line is invoiced or declared invoiced. A delivery
  note can be fully invoiced without carrying any invoice, when the policy
  declares every one of its lines invoiced.

The *To Be Invoiced* and *Invoiced* filters of the delivery note list, and the
*To invoice* filter of the delivery note line list, are restated in terms of
these fields, so a document closed by the policy is no more offered for
invoicing.

Deleting an invoice, or one of its lines, gives the delivery note lines it
was holding back to be invoiced. Those references are dropped by the database
itself, so nothing would otherwise tell the delivery note to evaluate its
lines again: a line would stay invoiced forever, it could no more be billed,
and its delivery note would keep showing as fully invoiced while carrying no
invoice at all.

The invoice reference of the delivery note is written whenever every line is
invoiced, whatever the run which invoiced it: the standard module writes it
only when one single run invoices every line, so a line invoiced separately -
or declared invoiced - used to leave the document open forever.

A delivery note which has nothing left to invoice is skipped by the invoicing
procedure instead of stopping it. Note that the mass invoicing wizard still
selects it - its domain belongs to `l10n_it_ddt` - but the delivery note is
now skipped instead of taking down the whole run. An error is raised only when
none of the selected delivery notes has anything to invoice.



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

10.0.0.1.0 (2026-09-01)
~~~~~~~~~~~~~~~~~~~~~~~

* [NEW] Initial implementation: bridge module between
  sale_order_line_qty_policy and l10n_it_ddt
* [NEW] Delivery note line flag force_invoiced and technical field
  line_invoiced
* [NEW] Delivery note field invoice_status
* [FIX] The invoice reference of the delivery note is written whenever every
  line is invoiced, no more only when every line was invoiced by one single
  run of the invoicing procedure
* [FIX] A delivery note with nothing to invoice is skipped by the invoicing
  procedure, so it no more stops the invoicing of the other ones
* [FIX] Deleting an invoice, or one of its lines, gives the delivery note
  lines back to be invoiced: the reference is dropped by the database, so the
  stored invoicing state was left behind and the line stayed invoiced forever
* [NEW] Italian translation



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
