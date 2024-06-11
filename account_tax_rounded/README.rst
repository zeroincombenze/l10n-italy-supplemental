=====================================================================
|icon| Account Invoice - Tax round/Arrotondamento IVA 10.0.12.0.0.1.0
=====================================================================

**Round taxes to comply italian laws**

.. |icon| image:: https://raw.githubusercontent.com/zeroincombenze/l10n-italy-supplemental/10.0/account_tax_rounded/static/description/icon.png


.. contents::



Overview | Panoramica
=====================

|en| This module evaluate invoices taxes to comply italian laws and avoid refuse from
Italian Tax Authority.

Odoo standard evaluate tax line by line and at the end sum all values. This behavior
produces a little difference between tax evaluated from total base and the sum of
taxes.

Look at the following example:

+------------------------+-----------+---------+-----------+-----------+-----------+-----------+
| Product                | Quantity  | Price   | Subtotal  | Tax Amoun | Sub.Round | Tax Round |
+------------------------+-----------+---------+-----------+-----------+-----------+-----------+
| Alpha                  | 50.00     | 0.1267  | 6.3350    | 1.3937    | 6.34      | 1.39      |
+------------------------+-----------+---------+-----------+-----------+-----------+-----------+
| Beta                   | 94.00     | 0.1167  | 10.9698   | 2.4134    | 10.97     | 2.41      |
+------------------------+-----------+---------+-----------+-----------+-----------+-----------+
| Gamma                  | 88.00     | 0.1210  | 10.6480   | 2.3426    | 10.65     | 2.34      |
+------------------------+-----------+---------+-----------+-----------+-----------+-----------+
| TOTAL (by SUM)         |           |         |           |           | 27.96     | 6.14      |
+------------------------+-----------+---------+-----------+-----------+-----------+-----------+
| TOTAL (Revaluated)     |           |         |           |           |           | 6.15      |
+------------------------+-----------+---------+-----------+-----------+-----------+-----------+



Odoo return the total base  27.96 (as sum of subtotal rounded)and total tax 6.14 (as
sum of taxes) but the total tax revaluate on 27.96 is 6.15

Odoo configuration "Round globally" solve when invoice is created but after update it
does not work.


|it| Questo modulo calcola l'IVA della fattura in modo da aderire alle leggi fiscali
italiane ed evitare il rifiuto dallo SdI.

Odoo calcola l'IVA riga per riga e al termine somma tutti i totali imponibili e IVA
delle singole righe. Questo comportamento produce una picola differenza tra il totale
dell'IVA ed il valore dell'IVA partendo dal totale imponibile.

Questo è un esempio:

+------------------------+-----------+---------+-----------+-----------+-----------+-----------+
| Product                | Quantity  | Price   | Subtotal  | Tax Amoun | Sub.Round | Tax Round |
+------------------------+-----------+---------+-----------+-----------+-----------+-----------+
| Alpha                  | 50.00     | 0.1267  | 6.3350    | 1.3937    | 6.34      | 1.39      |
+------------------------+-----------+---------+-----------+-----------+-----------+-----------+
| Beta                   | 94.00     | 0.1167  | 10.9698   | 2.4134    | 10.97     | 2.41      |
+------------------------+-----------+---------+-----------+-----------+-----------+-----------+
| Gamma                  | 88.00     | 0.1210  | 10.6480   | 2.3426    | 10.65     | 2.34      |
+------------------------+-----------+---------+-----------+-----------+-----------+-----------+
| TOTAL (by SUM)         |           |         |           |           | 27.96     | 6.14      |
+------------------------+-----------+---------+-----------+-----------+-----------+-----------+
| TOTAL (Revaluated)     |           |         |           |           |           | 6.15      |
+------------------------+-----------+---------+-----------+-----------+-----------+-----------+



Odoo restituisce il totale imponibile 27,96 (come somma di tutti gli imponibili delle
righe) e il totale IVA 6,14 (come somma dei totali IVA) ma il totale IVA calcolato da
27,96 è 6,15

Il parametro di configurazione "Arrotondare globalmente" è attivo solo in creazione ma
in modifica non funziona.


|thumbnail|

.. |thumbnail| image:: https://raw.githubusercontent.com/zeroincombenze/l10n-italy-supplemental/10.0/account_tax_rounded/static/description/description.png


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



Known issues | Roadmap
----------------------

This module replaces the standard Odoo function ``get_taxes_values()``
of the module *account*. The function, revaluate precisely the tax amound depending on
base amount. This behavior is due to avoid refusing invocie from Italian Tax Authority
which check tax amount MUST be: base amount * tax rate +/- 1 cent
For this reason, this module depends on specific 10.0.1.1.2 version of *account*



Proposals for enhancement
-------------------------

|en| If you have a proposal to change this module, you may want to send an email to <cc@shs-av.com> for initial feedback.
An Enhancement Proposal may be submitted if your idea gains ground.

|it| Se hai proposte per migliorare questo modulo, puoi inviare una mail a <cc@shs-av.com> per un iniziale contatto.



ChangeLog History | Cronologia modifiche
----------------------------------------

10.0.0.1.0 (2024-06-11)
~~~~~~~~~~~~~~~~~~~~~~~

* [IMP] First version
* [QUA] Test coverage 24% (29: 22+7) [0 TestPoints] - quality rating 15 (target 100)



FAQ | Domande & Risposte
------------------------

*I read about issue! May this module conflict with Odoo modules?*

No. This module is fully integrated with Odoo and OCA modules.
This module checks for Odoo module version. If Odoo module will be updated,
we will ASAP upgrade this module.



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

Last Update / Ultimo aggiornamento: 2024-06-11

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
