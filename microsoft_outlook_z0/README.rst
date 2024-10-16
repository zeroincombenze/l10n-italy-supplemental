=================================
|icon| Microsoft Outlook 10.0.1.1
=================================

**Microsoft Outlook Outgoing email server**

.. |icon| image:: https://raw.githubusercontent.com/zeroincombenze/l10n-italy-supplemental/10.0/microsoft_outlook_z0/static/description/icon.png


.. contents::



Overview | Panoramica
=====================

|en| This module adds the Outlook365 support for outgoing mail servers.
It is the backport from Odoo 12.0 module.


|it| Questo modulo fornisce il supporto per gestire un server e-mail in uscita
Outlook365.
Il modulo è un backport da Odoo 12.0.


|thumbnail|

.. |thumbnail| image:: https://raw.githubusercontent.com/zeroincombenze/l10n-italy-supplemental/10.0/microsoft_outlook_z0/static/description/description.gif


Configuration | Configurazione
------------------------------

Create a new application

To get started, go to Microsoft’s Azure Portal. Log in with the Microsoft Outlook Office
365 account if there is one, otherwise log in with the personal Microsoft account.
A user with administrative access to the Azure Settings will need to connect and
perform the following configuration.
Next, navigate to the section labeled Manage Microsoft Entra ID (formally Azure Active
Directory).

Now, click on Add (+), located in the top menu, and then select App registration.
On the Register an application screen, rename the Name to Odoo or something
recognizable. Under the Supported account types section select Accounts in any
organizational directory (Any Microsoft Entra ID directory - Multitenant) and personal
Microsoft accounts (e.g. Skype, Xbox).


Under the Redirect URL section, select Web as the platform, and then input
"https://<odoo base url>/microsoft_outlook/confirm" in the URL field.
The Odoo base URL is the canonical domain at which your Odoo instance can be reached
in the URL field.

Assign users and groups.

Create credentials.
Create "Client ID" and "Client secret" for successfully use into Odoo.

Setup in Odoo

☰ Settings > General Setting > Email

Set the alias domain to right value.

Load "Client ID" and "Client secret" created in Outlook365.

Activate the flag "Use external authentication provider"


☰ Settings > Activate the developer mode

☰ Settings > Technical > Emails > Outgoing Mail Server


To connect a Outlook365 mail server, set tha flag Outlook, check the smtp.server:
this module set smtp.outlook.com, however smtp server should be smtp.office365.com.
Port should be 587 and security should be "TLS (StartTLS)".
Set the user name but the password must be clean.

Save configuration than click on the right arrow to Connect your Outlook account.

A new window from Microsoft opens to complete the authorization process.
Select the appropriate email address that is being configured in Odoo.


Find mode info `Setup Odoo  in Microsoft Azure Portal<https://www.odoo.com/documentation/17.0/applications/general/email_communication/azure_oauth.html>`__



Usage | Utilizzo
----------------

if you have some trouble using this module, execute the following steps:


#. ☰ Settings > Activate the developer mode
#. ☰ Settings > Technical > Parameters > System parameters
#. Check for web.base.url value
#. ☰ Settings > General Setting > Email
#. Set the alias domain to right value
#. Check or reload "Client ID" and "Client secret"
#. ☰ Settings > Technical > Emails > Outgoing Mail Server
#. Repeat the "Connect your Outlook account" process



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

10.0.0.1.1 (2024-05-29)
~~~~~~~~~~~~~~~~~~~~~~~

* [FIX] Outlook authentication
* [QUA] Test coverage 34% (176: 116+60) [0 TestPoints] - quality rating 21 (target 100)

10.0.0.1.0 (2024-05-22)
~~~~~~~~~~~~~~~~~~~~~~~

* Initial implementation / Implementazione iniziale
* [QUA] Test coverage 34% (176: 116+60) [0 TestPoints] - quality rating 21 (target 100)



Credits | Ringraziamenti
========================

Copyright
---------

Odoo is a trademark of `Odoo S.A. <https://www.odoo.com/>`__ (formerly OpenERP)


Authors | Autori
----------------

* `SHS-AV s.r.l. <https://www.zeroincombenze.it>`__
* `Odoo SA <https://www.odoo.com>`__



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

Last Update / Ultimo aggiornamento: 2024-05-29

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
