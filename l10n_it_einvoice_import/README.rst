====================================================================================================================================
|icon| ITA - Fattura elettronica - Importazione fatture di vendita/Fattura elettronica - Importazione fatture di vendita 10.0.1.3.31
====================================================================================================================================

**E-invoice sale import**

.. |icon| image:: https://raw.githubusercontent.com/zeroincombenze/l10n-italy-supplemental/10.0/l10n_it_einvoice_import/static/description/icon.png


.. contents::



Overview | Panoramica
=====================

|en| This module creates **customer invoices** out of electronic invoice XML files
(FatturaPA version 1.2.1), the same job ``l10n_it_einvoice_in`` does for
supplier bills.

It is meant for sale invoices issued outside Odoo — produced by another
program, or downloaded back from the Exchange System (SdI) or from an
intermediary — which have to be registered in the accounting.

In the XML file the company is the *CedentePrestatore* and the customer is the
*CessionarioCommittente*: it is the other way round of a received bill. A file
whose *CedentePrestatore* is not the current company is refused.

For every customer it is possible to set the 'E-bills Detail Level':

 - Minimum level: invoice is created with no lines; user will have to create
   them, according to what specified in the electronic invoice
 - VAT code level: lines are cumulated by VAT code
 - Maximum level: every line contained in the electronic invoice creates a
   line in the invoice

Products are looked up by internal code or by description, since a sale
e-invoice carries the codes of the company itself. When no product is found,
the 'E-bill Default Product' of the customer is used.

Self billing documents (*autofattura*, TipoDocumento TD16 to TD23) are
imported too, but the roles in their header are swapped: the resulting invoice
is reported as an inconsistency, so that it can be checked by hand.

A whole zip file of e-invoices can be loaded at once, the way
``l10n_it_einvoice_import_zip`` does for purchase files; that module is left
to the purchase side, so neither has to depend on the other.


|it| Questo modulo crea le **fatture di vendita** a partire dai file XML di fattura
elettronica (FatturaPA versione 1.2.1), lo stesso lavoro che
``l10n_it_einvoice_in`` svolge per le fatture di acquisto.

È pensato per le fatture di vendita emesse fuori da Odoo — prodotte da un
altro programma, oppure riscaricate dal Sistema di Interscambio (SdI) o
dall'intermediario — che devono essere registrate in contabilità.

Nel file XML l'azienda è il *CedentePrestatore* e il cliente è il
*CessionarioCommittente*: esattamente l'opposto di una fattura ricevuta. Un
file il cui *CedentePrestatore* non è l'azienda corrente viene rifiutato.

Per ogni cliente è possibile impostare il 'Livello di dettaglio e-fattura':

 - Livello minimo: la fattura è creata senza righe; l'utente dovrà crearle in
   base a quanto indicato nella fattura elettronica
 - Livello aliquote: le righe sono cumulate per codice IVA
 - Livello massimo: ogni riga contenuta nella fattura elettronica genera una
   riga di fattura

I prodotti sono ricercati per codice interno o per descrizione, dato che una
e-fattura di vendita riporta i codici dell'azienda stessa. Se non viene
trovato alcun prodotto si usa il 'Prodotto predefinito e-fattura' del cliente.

Sono importate anche le autofatture (TipoDocumento da TD16 a TD23), ma i ruoli
nella loro testata sono invertiti: la fattura risultante viene segnalata tra le
incongruenze, così da poter essere verificata a mano.

È possibile caricare in una sola volta un intero file ZIP di fatture
elettroniche, come fa ``l10n_it_einvoice_import_zip`` per i file di acquisto;
quel modulo resta dedicato agli acquisti, così nessuno dei due deve dipendere
dall'altro.


|thumbnail|

.. |thumbnail| image:: https://raw.githubusercontent.com/zeroincombenze/l10n-italy-supplemental/10.0/l10n_it_einvoice_import/static/description/


Features | Caratteristiche
--------------------------

+--------------------------------------------------------+------------+------------------------------------+
| Descrizione                                            | Stato      | Note                               |
+--------------------------------------------------------+------------+------------------------------------+
| e-fattura di vendita, righe con IVA                    | |check|    |                                    |
+--------------------------------------------------------+------------+------------------------------------+
| e-fattura di vendita, righe senza IVA                  | |check|    | Non riconosce esatto codice IVA    |
+--------------------------------------------------------+------------+------------------------------------+
| e-fattura di vendita con ritenuta d'acconto            | |check|    |                                    |
+--------------------------------------------------------+------------+------------------------------------+
| e-fattura di vendita con controllo su totale fattura   | |check|    |                                    |
+--------------------------------------------------------+------------+------------------------------------+
| E-Nota Credito di vendita                              | |check|    | TD04 e TD08                        |
+--------------------------------------------------------+------------+------------------------------------+
| Autofattura (TD16-TD23)                                | |info|     | Importata, ruoli da verificare     |
+--------------------------------------------------------+------------+------------------------------------+
| e-fattura di vendita con split-payment                 | |no_check| |                                    |
+--------------------------------------------------------+------------+------------------------------------+
| Gestione multi-aziendale                               | |check|    |                                    |
+--------------------------------------------------------+------------+------------------------------------+
| Livello contabile solo testata senza dettagli          | |check|    | Per collegare fatture manuali      |
+--------------------------------------------------------+------------+------------------------------------+
| Livello righe contabili per aliquote IVA               | |check|    | Per fatture con troppe righe       |
+--------------------------------------------------------+------------+------------------------------------+
| Livelllo righe contabili in dettaglio                  | |check|    |                                    |
+--------------------------------------------------------+------------+------------------------------------+
| Ricerca prodotto per codice interno o descrizione      | |check|    |                                    |
+--------------------------------------------------------+------------+------------------------------------+
| Generazione scadenzario attivo da e-fattura            | |check|    |                                    |
+--------------------------------------------------------+------------+------------------------------------+



Configuration | Configurazione
------------------------------

A sale journal must exist for the company, and the customer must have a
receivable account: both are read when the invoice is created.

|menu| Accounting > Configuration > Settings

 - *Customer Payment Term*: whether the payment term of the imported invoice
   comes from the XML file or from the one assigned in the customer record
   (the default)
 - *Customer product search*: how to look the product up — by internal code,
   by exact name, or by similar name
 - *Rounding Tax on sale*: zero rate sale tax carrying the rounding line, when
   the totals of the XML file do not match the ones computed by Odoo. When not
   set, the purchase rounding tax of ``l10n_it_einvoice_in`` is used

The same two settings can be overridden per customer, in the partner form.

To see the forced number on the invoice form, the user must belong to the
*Allow to force invoice number* group of ``account_invoice_force_number``:
the number is written by the import in any case, the group only makes the
field visible.

Beware that an invoice carrying a forced number cannot be deleted, not even
while still in draft: this is standard Odoo behaviour for any invoice that has
been given a number. Cancel it instead.



Usage | Utilizzo
----------------

|menu| Accounting > Sales > E-invoice Export Files

 - Upload the XML file, or load a whole ZIP of them from
   |menu| Accounting > Sales > Electronic Invoice > Import eInvoice from ZIP,
   which is the sale counterpart of the same menu under Purchases
 - View the file content clicking on 'Preview'
 - Run the 'Import Sale Electronic Invoice' wizard to create the draft
   customer invoices

The list shows, for every file, how many invoices it contains and whether they
are already registered; the *Not registered* filter selects the files still to
be imported. A file the wizard has imported is flagged *Imported*, to tell it apart
from the ones this system generated out of its own invoices.

Whatever could not be matched — a tax code, a payment term, a product — is
written in the 'Import Inconsistencies' field of the created invoice, which is
left in draft state for review.

A file loaded here was already sent to the Exchange System by whoever produced
it, so it is marked as *Sent* as soon as it is uploaded, not only once it is
imported. Were it left in the *Ready to Send* state, the hourly send job of
``l10n_it_einvoice_send2sdi`` would send it to SdI a second time. Files this
system generates are untouched and stay *Ready to Send*.

To send such a file anyway, use the *Reset to ready* button on the file.

The number of the imported invoice is the one written in the xml file, forced
through the *Force Number* field of ``account_invoice_force_number``: the
document is already known to SdI and to the customer under that number, so the
sale journal sequence must not renumber it.



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

10.0.1.3.31 (2026-09-26)
~~~~~~~~~~~~~~~~~~~~~~~~

* [NEW] Import sale invoices from e-invoice xml file / Importazione fatture di vendita da file XML
* [IMP] Invoice number forced from xml file / Numero fattura forzato dal file XML
* [QUA] Test coverage 75% (394: 97+297) [0 TestPoints] - quality rating 43 (target 100)
* [IMP] Load sale e-invoices from a zip file / Caricamento e-fatture di vendita da file ZIP
* [IMP] Imported file is flagged as already sent to SdI / Il file importato è marcato come già inviato allo SdI



Credits | Ringraziamenti
========================

Copyright
---------

Odoo is a trademark of `Odoo S.A. <https://www.odoo.com/>`__ (formerly OpenERP)


Authors | Autori
----------------

* `SHS-AV s.r.l. <https://www.zeroincombenze.it>`__
* `Odoo Community Association (OCA) <https://odoo-community.org>`__



Contributors | Partecipanti
---------------------------

* `Lorenzo Battistini <lorenzo.battistini@agilebg.com>`__
* `Roberto Onnis <roberto.onnis@innoviu.com>`__
* `Alessio Gerace <alessio.gerace@agilebg.com>`__
* `Cesare Pellegrini <cesare@pointec.it>`__
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

Last Update / Ultimo aggiornamento: 2026-09-26

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
