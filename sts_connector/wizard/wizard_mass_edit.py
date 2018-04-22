# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class InvoiceXLSWizard(models.TransientModel):

    _name = 'invoice.xls.popup'

    # fields to generate xls
    date_from = fields.Date('Da data')
    date_to = fields.Date('A data')

    # fields for download xls
    state = fields.Selection([('choose', 'choose'), ('get', 'get')],
                             default='choose')
    report = fields.Binary('Prepared file', filters='.xml', readonly=True)
    name = fields.Char('File Name', size=32)

    @api.multi
    def generate_xls_report(self):
        openssl = OpenSSL('/opt/odoo/odoo/addons/invoice_xls_report/wizard/SanitelCF.cer')
        self.ensure_one()

        invoices = self.env['account.invoice'].search(
            [('type', '=', 'out_invoice'), ('date_invoice', '>=', self.date_from),
             ('date_invoice', '<=', self.date_to)])

        file = open("invoice.xml", "w")
        file.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' + '\n')
        file.write(
            '<precompilata xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="730_precompilata.xsd">' + '\n')

        #        file.write('\t' + '<proprietario>' + '\n' + '<cfProprietario>' + openssl.encrypt(str(invoice.company_id.vat)) + '</cfProprietario>' + '\n' + '\t' + '</proprietario>' + '\n')
        #        PdW9mZjfIVxncabWfE5dafCV1q5RUxr6343lMbWQdvKjq0SQ3bl0ulSyylnNjlVffXXfF2lH+2pR2nCBPExJDCapS+2Rln9C+IQrrQ+SroZw6M8YEHQZdgX2IJMKSxgJtuED0sbZFizfkYqasgZHI1Y4NkpKYQZeptdivd5KEjQ=

        file.write('\t' + '<proprietario>' + '\n')
        file.write('\t' + '\t' + '<codiceRegione>' + '604' + '</codiceRegione>' + '\n')
        file.write('\t' + '\t' + '<codiceAsl>' + '030' + '</codiceAsl>' + '\n')
        file.write('\t' + '\t' + '<codiceSSA>' + '000789' + '</codiceSSA>' + '\n')
        file.write('\t' + '\t' + '<cfProprietario>' + openssl.encrypt(
            str('PZZMMR56P41E801R').strip()) + '</cfProprietario>' + '\n')
        file.write('\t' + '</proprietario>' + '\n')

        for invoice in invoices:
            file.write('\t' + '<documentoSpesa>' + '\n')
            file.write('\t' + '\t' + '<idSpesa>' + '\n')
            file.write('\t' + '\t' + '\t' + '<pIva>' + (str(invoice.company_id.vat)[2:].strip()) + '</pIva>' + '\n')
            file.write('\t' + '\t' + '\t' + '<dataEmissione>' + invoice.date_invoice + '</dataEmissione>' + '\n')
            file.write('\t' + '\t' + '\t' + '<numDocumentoFiscale>' + '\n')
            file.write('\t' + '\t' + '\t' + '\t' + '<dispositivo>' + '1' + '</dispositivo>' + '\n')
            file.write('\t' + '\t' + '\t' + '\t' + '<numDocumento>' + str(invoice.number) + '</numDocumento>' + '\n')
            file.write('\t' + '\t' + '\t' + '</numDocumentoFiscale>' + '\n')
            file.write('\t' + '\t' + '</idSpesa>' + '\n')
            file.write('\t' + '\t' + '<dataPagamento>' + invoice.date_invoice + '</dataPagamento>' + '\n')
            file.write('\t' + '\t' + '<flagOperazione>' + 'I' + '</flagOperazione>' + '\n')
            file.write('\t' + '\t' + '<cfCittadino>' + openssl.encrypt(
                str(invoice.partner_id.function).strip()) + '</cfCittadino>' + '\n')
            file.write('\t' + '\t' + '<voceSpesa>' + '\n')
            #                file.write('\t' + '\t' + '\t' + '<tipoSpesa>' + (str(product_tmpl_id.x_tipospesa).strip()) + '</tipoSpesa>' + '\n')
            file.write('\t' + '\t' + '\t' + '<tipoSpesa>' + 'AD' + '</tipoSpesa>' + '\n')
            file.write('\t' + '\t' + '\t' + '<importo>' + str(invoice.amount_total) + '</importo>' + '\n')
            file.write('\t' + '\t' + '</voceSpesa>' + '\n')
            file.write('\t' + '</documentoSpesa>' + '\n')

        file.write('</precompilata>' + '\n')
        file.close()

        zipf = ZipFile("medico.zip", "w", zipfile.ZIP_DEFLATED)
        zipf.write("invoice.xml")
        zipf.close()

        src = 'medico.zip'
        dst = '/var/www/html/medico.zip'
        copyfile(src, dst)

        #        med = urllib.urlretrieve('http://localhost/medico.zip', 'zip.zip')

        return {
            'type': 'ir.actions.act_url',
            'url': 'http://173.212.203.37/medico.zip',
            'target': 'new'
        }




"""
    @api.multi
    def button_edit_data(self):
        \""" Upon confirmation data will be edited in all
            bank statement lines selected.\"""
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []
        for line in self.env['account.bank.statement.line'].browse(active_ids):
            if line.statement_id.state != ('confirm'):
                line.statement_id = self.statement_id.id

        return {"type": "ir.actions.act_window_close"}
        
    """
