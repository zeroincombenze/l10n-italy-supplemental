<html>
<head>
    <style type="text/css">
        ${css}

.list_bank_table {
    text-align:center;
    border-collapse: collapse;
    page-break-inside: avoid;
    display:table;
}

.act_as_row {
   display:table-row;
}
.list_bank_table .act_as_thead {
    background-color: #EEEEEE;
    text-align:left;
    font-size:10;
    font-weight:bold;
    padding-right:2px;
    padding-left:2px;
    white-space:nowrap;
    background-clip:border-box;
    display:table-cell;
}
.list_bank_table .act_as_cell {
    text-align:left;
    font-size:10;
    padding-right:2px;
    padding-left:2px;
    padding-top:1px;
    padding-bottom:1px;
    white-space:nowrap;
    display:table-cell;
}

.list_total_table {
    border:thin solid #E3E4EA;
    text-align:center;
    border-collapse: collapse;
}
.list_total_table td {
    border-top : thin solid #EEEEEE;
    text-align:left;
    font-size:10;
    padding-right:2px;
    padding-left:2px;
    padding-top:1px;
    padding-bottom:1px;
}
.list_total_table th {
    background-color: #EEEEEE;
    border: thin solid #000000;
    text-align:center;
    font-size:10;
    font-weight:bold;
    padding-right:2px;
    padding-left:2px;
}
.list_total_table thead {
    display:table-header-group;
}


    </style>
</head>
<body>
    <%page expression_filter="entity"/>
    <%
    def carriage_returns(text):
        return text.replace('\n', '<br />')
    %>

    <%def name="address(partner, commercial_partner=None)">
        <%doc>
            XXX add a helper for address in report_webkit module as this won't be suported in v8.0'
        </%doc>
        <% company_partner = False %>
        %if commercial_partner:
            %if commercial_partner.id != partner.id:
                <% company_partner = commercial_partner %>
            %endif
        %elif partner.parent_id:
            <% company_partner = partner.parent_id %>
        %endif

        %if company_partner:
            <tr><td class="name">${company_partner.name or ''}</td></tr>
            <tr><td>${partner.title and partner.title.name or ''} ${partner.name}</td></tr>
        %else:
            <tr><td class="name">${partner.title and partner.title.name or ''} ${partner.name}</td></tr>
        %endif
            <tr><td>${partner.street or ''}</td></tr>
            <tr><td>${partner.zip or ''} ${partner.city or ''}</td></tr>
            %if partner.country_id :
                <tr><td>${partner.country_id.name or ''} </td></tr>
            %endif

            %if partner.phone :
                <tr>
                    <td>${_("Tel.")} ${partner.phone}</td>
                        %if partner.fax :
                            <td>${_("Fax")}: ${partner.fax}</td>
                        %endif
                </tr>
            %endif             
            %if partner.email :
                <tr><td>${_("E-mail")}: ${partner.email}</td></tr>
            %endif
            %if partner.vat :
                <tr><td>${_("P.IVA")}: ${partner.vat}</td></tr>
            %endif
    </%def>

    %for inv in objects:
    <% setLang(inv.partner_id.lang) %>
    %if inv.type == 'out_invoice' :
        <div class="sender">
    %else :
        <div class="receiver">
    %endif
            <table class="recipient">
                <tr><td class="name">${inv.company_id.partner_id.name}</td></tr>
                <tr><td>${inv.company_id.partner_id.street or ''}</td></tr>
                <tr><td>${inv.company_id.partner_id.zip or ''} ${inv.company_id.partner_id.city or ''}</td></tr>
                %if inv.company_id.partner_id.country_id :
                <tr><td>${inv.company_id.partner_id.country_id.name or ''} </td></tr>
                %endif
                %if inv.company_id.partner_id.phone :
                <tr>
                    <td>${_("Tel.")} ${inv.company_id.partner_id.phone}</td>
                        %if inv.company_id.partner_id.fax :
                            <td>${_("Fax")}: ${inv.company_id.partner_id.fax}</td>
                        %endif
                </tr>
                %endif             
                %if inv.company_id.partner_id.email :
                <tr><td>${_("E-mail")}: ${inv.company_id.partner_id.email}</td></tr>
                %endif
                %if inv.company_id.partner_id.vat :
                <tr><td>${_("P.IVA")}: ${inv.company_id.partner_id.vat}</td></tr>
                %endif
            </table>
        </div>

    %if inv.type == 'out_invoice' :
        <div class="receiver">
    %else :
        <div class="sender">
    %endif
            <table class="recipient">
                %if hasattr(inv, 'commercial_partner_id'):
                    ${address(partner=inv.partner_id, commercial_partner=inv.commercial_partner_id)}
                %else:
                    ${address(partner=inv.partner_id)}
                %endif
            </table>
        </div>
    <h1 style="clear:both; padding-top: 10px;">
        %if inv.type == 'out_invoice' and inv.state == 'proforma2':
            ${_("PRO-FORMA")}
        %elif inv.type == 'out_invoice' and inv.state == 'draft':
            ${_("Draft Invoice")}
        %elif inv.type == 'out_invoice' and inv.state == 'cancel':
            ${_("Cancelled Invoice")} ${inv.number or ''}
        %elif inv.type == 'out_invoice':
            ${_("Invoice")} ${inv.number or ''}
        %elif inv.type == 'in_invoice':
            ${_("Supplier Invoice")} ${inv.number or ''}
        %elif inv.type == 'out_refund':
            ${_("Refund")} ${inv.number or ''}
        %elif inv.type == 'in_refund':
            ${_("Supplier Refund")} ${inv.number or ''}
        %endif
    </h1>
    %if inv.name :
        <h1 style="clear:both;">
            ${_("Subject : ")} ${inv.name or ''}
        </h1>
    %endif

    <table class="basic_table" width="100%">
        <tr>
            <th class="date">${_("Invoice Date")}</td>
            <th class="date">${_("Due Date")}</td>
            <th>${_("Responsible")}</td>
            <th>${_("Payment Term")}</td>
            <th>${_("Our reference")}</td>
        </tr>
        <tr>
            <td class="date">${formatLang(inv.date_invoice, date=True)}</td>
            <td class="date">${formatLang(inv.date_due, date=True)}</td>
            <td>${inv.user_id and inv.user_id.name or ''}</td>
            <td>${inv.payment_term and inv.payment_term.note or ''}</td>
            <td>${inv.origin or ''}</td>
        </tr>
    </table>

    <div>
    %if inv.note1:
        <p class="std_text"> ${inv.note1 | n} </p>
    %endif
    </div>

    <table class="list_table" width="100%" style="margin-top: 20px;">
      <thead>
        <tr>
            <th>${_("Cod.Articolo")}</th>          
            <th>${_("Description")}</th>
            <th>${_("UM")}</th>
            <th class="amount">${_("Quantity")}</th>
            <th class="amount">${_("Price")}</th>
            <th style="text-align:center;">${_("Taxes")}</th>
            <th class="amount">${_("Disc.(%)")}</th>
            <th class="amount">${_("Price")}</th> 
        </tr>
      </thead>
      <tbody>
        %for line in inv.invoice_line:
            <tr class="line">
                <td style="white-space: nowrap;" width="10%">${line.product_id.default_code or ''}</td>            
                <td>${ line.name }</td>
                <td style="white-space: nowrap;" width="6%">${line.uos_id and line.uos_id.name or ''}</td>
                <td class="amount" width="10%">${formatLang(line.quantity or 0.0,digits=get_digits(dp='Account'))}</td>
                <td class="amount" width="10%">${formatLang(line.price_unit)}</td>
                <td style="text-align:center;" width="8%">${ ', '.join([tax.description or tax.name for tax in line.invoice_line_tax_id])}</td>
                <td class="amount" width="8%">${line.discount and formatLang(line.discount, digits=get_digits(dp='Account')) or ''} ${line.discount and '%' or ''}</td>
                <td class="amount" width="14%">${formatLang(line.price_subtotal, digits=get_digits(dp='Account'))}&nbsp;${inv.currency_id.symbol}</td>
            </tr>
        %endfor
      </tbody>
      <tfoot>
      </tfoot>
    </table>

    %if inv.comment :
        <p style="margin-top: 6px;">${inv.comment | carriage_returns}</p>
    %endif

    <table class="total_table" width="100%">
        <tr>
            <td class="amount"><b>${_("Imponibile:")}</b></td>
            <td>${formatLang(inv.amount_untaxed, digits=get_digits(dp='Account'))} ${inv.currency_id.symbol}</td>     
            <td class="amount"><b>${_("Taxes:")}</b></td>
            <td>${formatLang(inv.amount_tax, digits=get_digits(dp='Account'))} ${inv.currency_id.symbol}</td>
            <td class="amount"><b>${_("Total:")}</b></td>
            <td>${formatLang(inv.amount_total, digits=get_digits(dp='Account'))} ${inv.currency_id.symbol}</td>
        </tr>
    </table>

        <br/>
    <table class="list_total_table" width="60%" >
        <tr>
            <th style="text-align:left;">${_("Rate")}</th>
            <th>${_("Base")}</th>
            <th>${_("Tax")}</th>
        </tr>
        %if inv.tax_line :
        %for t in inv.tax_line :
            <tr>
                <td style="text-align:left;">${ t.name } </td>
                <td class="amount" style="text-align:right;">${ formatLang(t.base, digits=get_digits(dp='Account')) }</td>
                <td class="amount" style="text-align:right;">${ formatLang(t.amount, digits=get_digits(dp='Account')) }</td>
            </tr>
        %endfor
        %endif
    </table>
    
    <p class="std_text"><b>${_("Dati di pagamento.")}</b></p>        
    
    <%
      inv_bank = inv.partner_bank_id
    %>
    <div class="list_bank_table act_as_table" style="width:100%;" >
      <!-- vat value are taken back from commercial id -->
        <div class="act_as_row">
            <div class="act_as_thead" style="width:8%;">${_("Bank")}</div>
            <div class="act_as_cell" style="width:80%;text-align:left;">${inv_bank and inv_bank.bank_name or '' } </div>
        </div>
        <div class="act_as_row">
            <div class="act_as_thead" style="width:8%;">${_("Bank account")}</div>
            <div class="act_as_cell" style="width:80%;text-align:left;">${ inv_bank and inv_bank.acc_number or '' }</div>
        </div>
        <div class="act_as_row">
            <div class="act_as_thead" style="width:8%;">${_("BIC")}</div>
            <div class="act_as_cell"  style="width:80%;text-align:left;">${inv_bank and inv_bank.bank_bic or '' }</div>
        </div>
    </div>
    <br/>

    %if inv.note2 :
        <p class="std_text">${inv.note2 | n}</p>
    %endif
    %if inv.fiscal_position and inv.fiscal_position.note:
        <br/>
        <p class="std_text">
        ${inv.fiscal_position.note | n}
        </p>
    %endif
    <p style="page-break-after:always"/>
    %endfor
</body>
</html>
