def migrate(cr, version):
    # update new sdi_state column with values from state
    cr.execute('UPDATE fatturapa_attachment_out SET sdi_state=state')
