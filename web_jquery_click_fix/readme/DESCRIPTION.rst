Since Chrome 89, browsers set ``event.button`` on click events in a way that the
jQuery 1.11.1 shipped with Odoo 10 does not expect: some delegated clicks are
dropped and buttons or links in the web client do not respond.

This module loads a patched copy of jQuery 1.11.1 instead of the standard one.
The only change is the delegated-event check in ``jQuery.event.handlers``.
The module is installed automatically together with ``web``.
