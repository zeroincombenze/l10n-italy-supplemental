============================================================
|icon| Send E-Invoice to SdI/Invio fatture a SdI 10.0.1.0.56
============================================================

**Send E-Invoice to customer through SdI**

.. |icon| image:: https://raw.githubusercontent.com/zeroincombenze/l10n-italy-supplemental/10.0/l10n_it_einvoice_send2sdi/static/description/icon.png


.. contents::



Overview | Panoramica
=====================

|en| This module can send Italian e-invoices to Customer through
`Sdi <http://www.fatturapa.gov.it/export/fatturazione/it/sdi.htm>`__


|it| Questo modulo permette di inviare le fatture tramite uno canale
`Sdi <http://www.fatturapa.gov.it/export/fatturazione/it/sdi.htm>`__

In questa versione è implementato uno specifico canale JSON verso hub di
terzo incaricato e il canale PEC.


|thumbnail|

.. |thumbnail| image:: https://raw.githubusercontent.com/zeroincombenze/l10n-italy-supplemental/10.0/l10n_it_einvoice_send2sdi/static/description/description.png


Configuration | Configurazione
------------------------------

☰ Accounting > Configuration > Accounting > Tax Authority Definition > Sender Channel

Values:

* SDI Channel = JSON
* Client ID = *Supplied by Evolve*
* Client key = *Supplied by Evolve*
* URL Sender = https://www.certdoc.it/rest/api/v1/
* Company ID = *Supplied by Evolve*
* Custom1 = *Evolve out channel* (default 1)
* Custom2 = *Evolve in channel* (default 2)
* Custom3 = *Evolve sent channel* (default 3)
* Custom4 = # day before today to read (max 60), (default 59)

Warning: Custom4 > 0 and < 60 disable downloaded flag



Usage | Utilizzo
----------------

Click on button [Invia a Sdi]



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

10.0.1.0.56 (2025-07-19)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Move from repo l10n-italy
* [QUA] Test coverage 15% (833: 707+126) [1 TestPoints] - quality rating 12 (target 100)

10.0.1.0.55 (2025-05-27)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Received filename .xml.p7m are equal to .xml / File firmati equiparati a non firmati
* [IMP] Search incremental documents / Ricerca incrementale dei documenti
* [QUA] Test coverage 15% (833: 707+126) [1 TestPoints] - quality rating 12 (target 100)

10.0.1.0.54 (2025-05-15)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] New domain mode based on invoice date
* [QUA] Test coverage 15% (824: 697+127) [1 TestPoints] - quality rating 10 (target 100)

10.0.1.0.53 (2025-03-14)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Minor improvements
* [QUA] Test coverage 15% (821: 694+127) [1 TestPoints] - quality rating 10 (target 100)

10.0.1.0.52 (2025-02-18)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Minor improvements
* [QUA] Test coverage 15% (821: 694+127) [1 TestPoints] - quality rating 10 (target 100)


10.0.1.0.51 (2025-01-13)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] New Evolve PA states / Nuovi stati fattura PA
* [QUA] Test coverage 15% (821: 694+127) [1 TestPoints] - quality rating 10 (target 100)

10.0.1.0.50 (2024-12-12)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] New Evolve PA states / Nuovi stati fattura PA
* [QUA] Test coverage 15% (821: 694+127) [1 TestPoints] - quality rating 10 (target 100)

10.0.1.0.49 (2024-09-09)
~~~~~~~~~~~~~~~~~~~~~~~~

* [QUA] Test coverage 15% (817: 692+125) [0 TestPoints] - quality rating 10 (target 100)

10.0.1.0.48 (2024-08-29)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Send by cron / Invio fatture schedulato
* [QUA] Test coverage 15% (817: 692+125) [0 TestPoints] - quality rating 10 (target 100)

10.0.1.0.46 (2024-08-07)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Minor improvements
* [QUA] Test coverage 15% (812: 688+124) [1 TestPoints] - quality rating 10 (target 100)

10.0.1.0.45 (2024-07-03)
~~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] Minor improvements
* [QUA] Test coverage 15% (814: 688+126) [1 TestPoints] - quality rating 10 (target 100)

10.0.1.0.44 (2024-05-14)
~~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Invoice rejected in some cases
* [QUA] Test coverage 15% (814: 688+126) [1 TestPoints] - quality rating 10 (target 100)



Credits | Ringraziamenti
========================

Copyright
---------

Odoo is a trademark of `Odoo S.A. <https://www.odoo.com/>`__ (formerly OpenERP)


Authors | Autori
----------------

* `SHS-AV s.r.l. <https://www.zeroincombenze.it>`__
* `Pointec s.r.l. <https://www.pointec.it>`__



Contributors | Partecipanti
---------------------------

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

Last Update / Ultimo aggiornamento: 2025-07-19

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
