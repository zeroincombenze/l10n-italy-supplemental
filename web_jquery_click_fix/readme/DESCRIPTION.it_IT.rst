Da Chrome 89, i browser impostano ``event.button`` sugli eventi click in un modo
non previsto da jQuery 1.11.1 incluso in Odoo 10: alcuni click delegati vengono
persi e pulsanti o link del client web non rispondono.

Questo modulo carica una copia corretta di jQuery 1.11.1 al posto di quella
standard. L'unica modifica è il controllo degli eventi delegati in
``jQuery.event.handlers``. Il modulo si installa automaticamente con ``web``.
