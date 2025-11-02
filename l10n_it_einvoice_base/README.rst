=============================================================
|icon| EInvoice + FatturaPA/l10n_it_einvoice_base 10.0.2.1.27
=============================================================

**Infrastructure for Italian Electronic Invoice + FatturaPA**

.. |icon| image:: https://raw.githubusercontent.com/zeroincombenze/l10n-italy/10.0/l10n_it_einvoice_base/static/description/icon.png


.. contents::



Overview | Panoramica
=====================

|en| This module manage infrastructure to manage Italian E Invoice and FatturaPA
as per send to the SdI (Exchange System by Italian Tax Authority)

`Italian e-invoice laws <https://www.agenziaentrate.gov.it/portale/normativa-prassi-e-regole-tecniche-fatture-elettroniche>`__


|it| Questo modulo gestisce l'infrastruttura per generare il file xml della Fattura
Elettronica e della FatturaPA, versione 1.2.1, da trasmettere al sistema di
interscambio SdI.

In anagrafica clienti i dati per la fattura elettronica sono inseribili nella
scheda "Agenzia delle Entrate".


Destinatari
-----------

Il modulo è destinato a tutte le aziende che dal 2019 emettono fattura elettronica

Normativa
---------

Le leggi inerenti la fattura elettronica sono numerose. Potete consultare
la `normativa fattura elettronica <https://www.agenziaentrate.gov.it/portale/normativa-prassi-e-regole-tecniche-fatture-elettroniche>`__


Fattura elettronica a soggetto IVA
----------------------------------

Installare il modulo *l10n_it_einvoice_out*

Si tratta della casistica più comune. Selezionare "Soggetto a fattura elettronica"
e compilare il "Codice destinatario" o la "PEC".
La partita IVA è un dato obligatorio ai fini dell'invio.
L'eventuale invio di una fattura in formato PDF è una fattura di cortesia e non
ha valore legale.

Fattura elettronica a PA
------------------------

Installare il modulo *l10n_it_einvoice_out*

Questa casistica è attiva già dal 2016. Impostare "Pubblica Amministrazione"
e compilare il "Codice ufficio". Prestare attenzione alla normativa sulla scissione dei
pagamenti e all'inserimento dei dati aggiuntivi CIG e CUP.

Fattura elettronica da DdT (TD24)
---------------------------------

Installare il modulo *l10n_it_einvoice_ddt*

Fattura elettronica a privato senza partita IVA
-----------------------------------------------

Installare il modulo *l10n_it_einvoice_out*

La legge non prevede l'obbligo di emissione della fattura elettronica ma è
ammessa l'emissione a condizione che venga inviata una fattura in formato PDF
al cliente. Inserire il valore "0000000" nel codice destinatario e il codice fiscale.


Fattura elettronica a soggetto IVA senza Codice Destinatario ne PEC
-------------------------------------------------------------------

Installare il modulo *l10n_it_einvoice_out*

Casistica in cui un cliente con partita IVA che non abbia fornito
ne il proprio Codice Destinatario ne la propria PEC. Si riconduce al caso
precedente, inserendo il valore "0000000" nel codice destinatario ed il
codice fiscale. Anche in questo caso è obbligatorio inviare una fattura in
formato PDF al cliente.

Fattura elettronica a rappresentante fiscale in Italia
------------------------------------------------------

Installare il modulo *l10n_it_einvoice_out*

Casistica di aziende estere con rappresentanza fiscale in Italia.
Inserire nei contatti un indirizzo di fatturazione di tipo "Rappresentante fiscale"
con la partita IVA italiana ed i dati per la fatturazione elettronica.
La fattura va emessa al rappresentante fiscale.

Fattura elettronica a stabile organizzazione
--------------------------------------------

Installare il modulo *l10n_it_einvoice_out*

Casistica di aziende estere con stabile organizzazione in Italia.
Inserire nei contatti un indirizzo di fatturazione di tipo "Stabile organizzazione"
con la partita IVA italiana ed i dati per la fatturazione elettronica.
La fattura va emessa alla stabile organizzazione.

Fattura elettronica a soggetto estero
-------------------------------------

Installare il modulo *l10n_it_einvoice_out*

Inserire il valore XXXXXXX nel codice destinatario. Il file XML viene generato
con le opportune correzioni per la validazioni dell'Agenzia delle Entrate.
Anche in questo caso è obbligatorio inviare una fattura in formato PDF al cliente.

Se il soggetto non ha ne partita IVA ne codice fiscale, nella fattura elettronica
viene inserita una partita IVA convenzionale "%(iso)s99999999999" con il codice ISO
della nazione cliente e 11 cifre '9'.

Il campo CAP viene convenzionalmente compilato con "00000" e la provincia con "EE".

Emissione fattura con dichiarazione di intento
----------------------------------------------

Installare il modulo *l10n_it_einvoice_li*

Inserire il riferimento della lettera di intento.


Emissione auto-fattura
----------------------

Casistica per fatture ricevute in regime di reverse charge (tipi documento da TD16 a
TD19) oppure per emissione auto-fatture per integrazione (TD20, TD21, TD25, TD27 e
TD28). Per l'emissione delle autofatture in regime di reverse charge, installare il
modulo *l10n_it_einvoice_out_rc* mentre l'emissione di auto-fatture in integrazione
installare il modulo *l10n_it_einvoice_out*


|thumbnail|

.. |thumbnail| image:: https://raw.githubusercontent.com/zeroincombenze/l10n-italy/10.0/l10n_it_einvoice_base/static/description/description.png


Certifications | Certificazioni
-------------------------------

+----------------------+------------------------------------------------------------------------------------------------------+---------------+--------------+----------------------------------------------+
| Logo                 | Ente/Certificato                                                                                     | Data inizio   | Da fine      | Note                                         |
+----------------------+------------------------------------------------------------------------------------------------------+---------------+--------------+----------------------------------------------+
| |xml\_schema|        | `ISO + Agenzia delle Entrate <https://www.fatturapa.gov.it/export/fatturazione/it/strumenti.htm>`__  | 01-06-2017    | 31-12-2024   | Validazione contro schema xml                |
+----------------------+------------------------------------------------------------------------------------------------------+---------------+--------------+----------------------------------------------+
| |FatturaPA|          | `FatturaPA <https://www.fatturapa.gov.it/export/fatturazione/it/index.htm>`__                        | 01-06-2017    | 31-12-2024   | Controllo tramite sito Agenzia delle Entrate |
+----------------------+------------------------------------------------------------------------------------------------------+---------------+--------------+----------------------------------------------+



Configuration | Configurazione
------------------------------

☰  Configuration > Configuration > Invoicing > Fattura PA

☰  Invoicing > Configuration > Tax > Tax > Set Nature

☰  Invoicing > Configuration > Management > Payment Terms

☰  Invoicing > Customers > Customers > Set data

☰  Invoicing > Configuration > Invoicing > Fiscal Positions

Read only:

☰  Invoicing > Configuration > Invoicing > IRS definition > Tax natue

☰  Invoicing > Configuration > Invoicing > IRS definition > Invoice type



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
    deploy_odoo clone -r l10n-italy -b 10.0 -G zero -p $HOME/10.0
    # Upgrade virtual environment
    vem amend $HOME/10.0/venv_odoo



Upgrade | Aggiornamento
-----------------------

::

    deploy_odoo update -r l10n-italy -b 10.0 -G zero -p $HOME/10.0
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
<https://github.com/zeroincombenze/l10n-italy/issues>`_.

In case of trouble, please check there if your issue has already been reported.



Known issues | Roadmap
----------------------

|en| Please, do not mix the following module with OCA Italy modules.

This module may be conflict with some OCA modules with error:

|exclamation| name CryptoBinary used for multiple values in typeBinding


|it| Si consiglia di non mescolare i seguenti moduli con i moduli di OCA Italia.

Lo schema di definizione xml, pubblicato con
urn:www.agenziaentrate.gov.it:specificheTecniche è base per tutti i file
in formato xml da inviare all'Agenzia delle Entrate; come conseguenza
nasce un conflitto tra moduli diversi che utilizzano uno schema che riferisce
all'urn dell'Agenzia delle Entrate, di cui sopra, segnalato dall'errore:

|exclamation| name CryptoBinary used for multiple values in typeBinding

* This module replaces l10n_it_fatturapa of OCA distribution.
* Do not use l10n_it_base module of OCA distribution
* Do not use l10n_it_split_payment module of OCA distribution
* Do not use l10n_it_reverse_charge of OCA distribution
* Do not install l10n_it_codici_carica module of OCA distribution
* Do not install l10n_it_fiscal_document_type module of OCA distribution
* Do not install l10n_it_fiscalcode_invoice module of OCA distribution
* Do not install l10n_it_ipa module of OCA distribution
* Do not install l10n_it_esigibilita_iva of OCA distribution



Proposals for enhancement
-------------------------

|en| If you have a proposal to change this module, you may want to send an email to <cc@shs-av.com> for initial feedback.
An Enhancement Proposal may be submitted if your idea gains ground.

|it| Se hai proposte per migliorare questo modulo, puoi inviare una mail a <cc@shs-av.com> per un iniziale contatto.



ChangeLog History | Cronologia modifiche
----------------------------------------

10.0.2.1.27 (2024-07-30)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] welfare.fund description
* [QUA] Test coverage 61% (516: 202+314) [0 TestPoints] - quality rating 37 (target 100)

10.0.2.1.26 (2024-07-16)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] New field efatt_xml_rounding
* [QUA] Test coverage 61% (516: 202+314) [0 TestPoints] - quality rating 37 (target 100)

10.0.2.1.25 (2024-03-09)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Field carrier_id conflicts with other modules
* [QUA] Test coverage 61% (515: 202+313) [0 TestPoints] - quality rating 37 (target 100)

10.0.2.1.24 (2024-02-01)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Sender on invoice header / Soggetto emittente in testata fattura
* [QUA] Test coverage 61% (515: 202+313) [0 TestPoints] - quality rating 37 (target 100)

10.0.2.1.23 (2023-03-08)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Fiscal document type for refund / TD04 per note credito

10.0.2.1.22 (2023-02-13)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Self invoice flag / Identificatore documento autofattura
* [IMP] Date updatable for self invoice / Data contabile modificabile per le auto-fatture

10.0.2.1.21 (2022-11-14)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Company data view with name for field extentions



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

* `Antonio Maria Vigliotti <antoniomaria.vigliotti@gmail.com>`__



Acknowledges | Riconoscimenti
-----------------------------

* `Odoo Italia Network <https://www.odoo-italia.net>`__
* `Davide Corio <davide.corio@abstract.it>`__
* `Lorenzo Battistini <lorenzo.battistini@agilebg.com>`__



Translations by | Traduzioni a cura di
--------------------------------------

* `Sergio Zanchetta <https://github.com/primes2h>`__
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

This module is part of l10n-italy project.

Last Update / Ultimo aggiornamento: 2024-07-30

.. |Maturity| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
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
