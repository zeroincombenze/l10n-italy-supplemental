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
