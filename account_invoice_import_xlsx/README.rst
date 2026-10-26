=========================================================================
|icon| Import file Excel into invoice/Importa fatture da Excel 18.0.1.0.0
=========================================================================

**Import invoice from Excel file**

.. |icon| image:: https://raw.githubusercontent.com/zeroincombenze/l10n-italy-supplemental/18.0/account_invoice_import_xlsx/static/description/icon.png


.. contents::



Overview | Panoramica
=====================

|en| This module imports invoice data from an Excel (.xlsx) file in two ways:

* **Import lines into an invoice**: the button [Import xlsx] on a draft invoice or
  vendor bill adds one line per row of the file. Products are searched by code and
  name; price, account and taxes come from the product unless the file supplies them.
* **Create invoices**: the menu *Accounting › Configuration › Import Account Invoice*
  creates draft invoices. A row with customer data starts a new invoice; rows
  without customer data add lines to it.

Recognized column titles:

* ``Denominazione Cliente``: Partner name
* ``Partita Iva``: Partner VAT number (``IT`` is added to digits only)
* ``Codice Fiscale``: Partner fiscal code
* ``Codice``: Product code
* ``Nome``: Line description
* ``Quantita``: Quantity
* ``Imponibile``: Taxable amount (line with quantity 1)
* ``Iva``: Tax amount; nearest rate among 0, 4, 5, 10, 22% is used
* ``Numero``: Invoice number
* ``Data``: Invoice date (dd/mm/yyyy or Excel date)

Numbers can be written in Italian format (``2.049,18``).
You can find Excel examples in the example directory.


|it| Questo modulo importa dati di fattura da un file Excel (.xlsx) in due modi:

* **Importa righe in una fattura**: il bottone [Import xlsx] su una fattura o fattura
  fornitore in bozza aggiunge una riga per ogni riga del file. I prodotti sono cercati
  per codice e nome; prezzo, conto e imposte derivano dal prodotto, se il file non li
  indica.
* **Crea fatture**: il menù *Contabilità › Configurazione › Import Account Invoice*
  crea fatture in bozza. Una riga con i dati del cliente apre una nuova fattura; le
  righe senza dati del cliente vi aggiungono righe.

Titoli di colonna riconosciuti:

* ``Denominazione Cliente``: Nome del soggetto
* ``Partita Iva``: Partita IVA (alle sole cifre viene anteposto ``IT``)
* ``Codice Fiscale``: Codice fiscale
* ``Codice``: Codice prodotto
* ``Nome``: Descrizione della riga
* ``Quantita``: Quantità
* ``Imponibile``: Imponibile (riga con quantità 1)
* ``Iva``: Importo IVA; aliquota più vicina tra 0, 4, 5, 10, 22%
* ``Numero``: Numero fattura
* ``Data``: Data fattura (gg/mm/aaaa o data Excel)

I numeri possono essere scritti in formato italiano (``2.049,18``).
Si possono vedere esempi nella cartella example.


|thumbnail|

.. |thumbnail| image:: https://raw.githubusercontent.com/zeroincombenze/l10n-italy-supplemental/18.0/account_invoice_import_xlsx/static/description/


Usage | Utilizzo
----------------

* Open a draft invoice or vendor bill and click [Import xlsx]; choose the file and
  click [Import]. Tick *Dry-run* to check the file without creating anything.
* To create invoices, open *Accounting › Configuration › Import Account Invoice*,
  choose the file, the journal (sale or purchase) and the default invoice date. The
  result window lists the rows with problems (partner or product not found, more
  than one match).
* Invoices are always created in draft: check and confirm them as usual.



Getting started | Primi passi
=============================

|Try Me|


Prerequisites | Prerequisiti
----------------------------

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
| $HOME/18.0 |
+----------------------------------------------------------------------------+

::

    # Odoo repository installation; OCB repository must be installed
    deploy_odoo clone -r l10n-italy-supplemental -b 18.0 -G zero -p $HOME/18.0
    # Upgrade virtual environment
    vem amend $HOME/18.0/venv_odoo



Upgrade | Aggiornamento
-----------------------

::

    deploy_odoo update -r l10n-italy-supplemental -b 18.0 -G zero -p $HOME/18.0
    vem amend $HOME/18.0/venv_odoo
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

18.0.1.0.0 (2026-10-25)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Migrated to Odoo 18.0 / Migrazione a Odoo 18.0
* [FIX] Date read from file: no more padding with spaces / Data da file: niente più spazi
* [FIX] Tax rate: nearest rate is used / Aliquota IVA: viene usata l'aliquota più vicina
* [FIX] Numbers are not evaluated as Python code anymore / I numeri non sono più valutati come codice Python
* [IMP] Lines can be imported only into draft invoices / Le righe si importano solo in fatture in bozza

18.0.0
~~~~~~

* [FIX] User no admin can import / Utenti non admin possono importare
* [FIX] Evaluate early total tax / Calcolo totale IVA immediato
* [IMP] Use listprice, if present / Utilizza listino se presente (richiede modulo aggiuntivo)



Credits | Ringraziamenti
========================

Copyright
---------

Odoo is a trademark of `Odoo S.A. <https://www.odoo.com/>`__ (formerly OpenERP)


Authors | Autori
----------------

* `Zeroincombenze srls <https://www.zeroincombenze.it>`__



Contributors | Partecipanti
---------------------------

* `Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>`__



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

Last Update / Ultimo aggiornamento: 2026-10-26

.. |Maturity| image:: https://img.shields.io/badge/maturity-Alfa-black.png
    :target: https://odoo-community.org/page/development-status
    :alt: 
.. |license gpl| image:: https://img.shields.io/badge/licence-LGPL--3-7379c3.svg
    :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
    :alt: License: LGPL-3
.. |license opl| image:: https://img.shields.io/badge/licence-OPL-7379c3.svg
    :target: https://www.odoo.com/documentation/user/14.0/legal/licenses/licenses.html
    :alt: License: OPL
.. |Try Me| image:: https://www.zeroincombenze.it/wp-content/uploads/ci-ct/prd/button-try-it-18.svg
    :target: https://erp18.zeroincombenze.it
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
