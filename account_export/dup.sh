echo "\$ rm -fR /opt/odoo/8.0/__to_remove/l10n_it_ade/"
rm -fR /opt/odoo/8.0/__to_remove/l10n_it_ade/
echo "\$ mv /opt/odoo/8.0/l10n-italy/l10n_it_ade/ /opt/odoo/8.0/__to_remove/"
mv /opt/odoo/8.0/l10n-italy/l10n_it_ade/ /opt/odoo/8.0/__to_remove/
echo "\$ cp -R /opt/odoo/7.0/l10n-italy/l10n_it_ade/ /opt/odoo/8.0/l10n-italy/"
cp -R /opt/odoo/7.0/l10n-italy/l10n_it_ade/ /opt/odoo/8.0/l10n-italy/
# echo "cp /opt/odoo/8.0/__to_remove/l10n_it_ade/bindings/* /opt/odoo/8.0/l10n-italy/l10n_it_ade/bindings/"
# cp /opt/odoo/8.0/__to_remove/l10n_it_ade/bindings/* /opt/odoo/8.0/l10n-italy/l10n_it_ade/bindings/
echo "\$ sed 's/7\.0/8.0/' -i /opt/odoo/8.0/l10n-italy/l10n_it_ade/__openerp__.py" 
sed 's/7\.0/8.0/' -i /opt/odoo/8.0/l10n-italy/l10n_it_ade/__openerp__.py
echo "mv /opt/odoo/8.0/l10n-italy/l10n_it_ade/static/src/img /opt/odoo/8.0/l10n-italy/l10n_it_ade/static/description"
mv /opt/odoo/8.0/l10n-italy/l10n_it_ade/static/src/img /opt/odoo/8.0/l10n-italy/l10n_it_ade/static/description
echo "rm -fR /opt/odoo/8.0//l10n-italy/l10n_it_ade/static/src/"
rm -fR /opt/odoo/8.0//l10n-italy/l10n_it_ade/static/src/
