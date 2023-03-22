# -*- coding: utf-8 -*-

from odoo import models, fields, api
import os
import json
from cryptography.hazmat.primitives import hashes,  serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.backends import default_backend
import base64
from datetime import datetime
import odoo
import io

PRIVATE_KEY = """
-----BEGIN PRIVATE KEY-----
MIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQDJBdFK/VqGDYWT
g/fSfDWNK4dfpt47SILcars09i1di1AbsbZS4RHdcxkC2b3ElmMvsqKve9Pk9SeW
qHYXAENAAxZE2iEuq35S01RBMg9fOCdEmglDFs+nEdGK/jYjxSOSeTYgWu+9zUv8
aEPSytWRUZv7UtWBRmOHPMvDBRFff583+80gpmMzf1DY7zK35qe0YlrQ4lVOBK5b
yN3AEl31WaFOPex+vdC6PbZo7N1ZAoai1Hpz6NWN9RZDo8RlW4qBoTWWcrF1L96t
KDti6cvYIwcANfu0yNINIecZq7AjCyDGpAHO65bM1R6LKqsbo8/GTxB3tHOqQpd5
udXaa7/xAgMBAAECggEALK20VLx2sDC1LZI5NHkS1euEzQejgP2eyCqYrS7B6naa
OW2IHmeTtupr9qw6d0UNin5jlikpcUvjnqKWjIosaD/HZUot8dd/3hzGLy9XJ0yt
vZuWz2h0gqd9MS1LDywzucxi8VIE0uScLN9no6QdT40Z5AQHHBJu8JHcn92yfMzV
bzwR688vKpw+eTIwU7+ZHS4OEg9aS1Kh+kjnAnk9o4dQDCv30oBm/jT8nCFdz3nX
3/Oy3qwcXeyU97iV/HlytrDo11zDT7an10eh38yje7oO0L5hBPFbmdKZWQbVIQ2G
R5l/TWgtW/Nytc0GYMc2YBtqSoYM1/KkZF6v//GnoQKBgQD4YaDZpkLc15docFSk
AAmjiDJEc/6MuepqectO7d7Q3YdKN6sSfsRJ2ZTjAoB++RUYwImmAui+H4y+smvR
CxsGRdCIRhO/TSI53gDKiZkVHpXRuZId0uVkRBlEIhwhVwrYZPla1PcCil/9NWfc
afnROC2wv7Hn1lLJh8oIwAVP5QKBgQDPMFBQu+y8EoW2wEHPrVrN4wT4lqblmdDZ
L3JE+y6pzCBPpTam/Q2kSadnyQU9EpFPw4ISXqt3ZCCDo/Ynfz15BKu+AW4eeQFQ
WBLtiYPVwZLtlx0IvhlFBnkY3i3WS3HdgTNNC8AoEIekkIB5vTNXdl9WQ7ECLdxB
QW2HCZG3HQKBgQDT7Qj/bBr0r4bid6XgYJ/YxmaNfaMdk6vtuYm9CLzq3XmH28O9
fighEuM0ZngY3pIfknhgC29meSjvtPDFZoJiccMh4xkKStf/I+rs5UaWfIg8b+e6
Rq2vRWOBfNEfqVL5m/4egENaCZMpSx4ZNNsQpqxleMplE7uDdLbvjFd7+QKBgQCD
deVQBJ1GC/6ZoU1gp175SfVKgdRt1HYGiCtaB4JpLGLIBk0yEVhJiI5WtN7FDHX1
BVkPrM/hFj/nJu61yu9HTSZnjeLAJQknYGrKGznyNDu00vASLwQ7nsrRc4/j68TY
xfS2CyGmii52xVUvaVQdR7dgNd0nQ8//+7KyPukdJQKBgQCIzq5y0y5UkNMX0pBt
0XTXxQYwMNyGqDnMVaxqyOeXs3EQ61t85kA5gMznMSsMhNuoYF8w0JKQNKXeKjE7
UL87UIMIGZxfr1sVJA6gLegi2P6Pbwucf0vIUhy8+fJup7zHRJWSwkjIaVVL5viG
xdLNFPzmyh6Hs/CuVF+Rc/6r4Q==
-----END PRIVATE KEY-----
"""

class LicenseVerification(models.Model):
    _name = 'license_verification'

    license_key = fields.Char(string="Chiave Licenza", invisible=True)
    expiry_date = fields.Date(string="Scadenza Licenza", help="Scadenza Licenza", readonly=True)
    n_users = fields.Integer(string="Numero di utenti", readonly=True)
    license_file = fields.Binary(string='File di licenza')

    @api.model
    def create(self, vals):
        #Get database id
        db_id = self.env['ir.config_parameter'].get_param('database.uuid')
        #Read key
        # path = os.path.dirname(os.path.abspath(__file__))
        # path_join = os.path.normpath(os.path.join(path, '..', 'private_key.pem'))
        # with open(path_join, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            str.encode(io.StringIO(PRIVATE_KEY).read()),
            password=None,
            backend=default_backend()
        )
        decodedtext = bytes.fromhex(base64.b64decode(vals['license_file']).decode())
        decrypted = private_key.decrypt(
            decodedtext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        obj_license = json.loads(decrypted.decode('utf-8').replace("\'", "\""))
        #Check database id
        if obj_license['database_id'] != db_id:
            raise UserWarning('ID del database non corretto')
        vals['n_users'] = obj_license['n_users']
        vals['expiry_date'] = obj_license['expiry_date']
        return super(LicenseVerification, self).create(vals)

    @api.model
    def verify_license(self):
        # Check all licenses
        user_counter = 0
        MAX_USERS = 0
        if len(self) == 0:
            raise odoo.exceptions.AccessDenied('Accesso non autorizzato per mancanza di licenza')
        for license in self:
            #Check if the database id hasn't changed
            db_id = self.env['ir.config_parameter'].get_param('database.uuid')
            #Read base64 uploaded file
            decodedtext = bytes.fromhex(base64.b64decode(license.license_file).decode())
            decrypted = self.decrypt_license(decodedtext)
            obj_license = json.loads(decrypted.decode('utf-8').replace("\'", "\""))
            # Check database id
            if obj_license['database_id'] != db_id:
                raise odoo.exceptions.AccessDenied('Impossibile accedere per problemi nella licenza: ID del database non corretto')
            MAX_USERS += obj_license['n_users']
            users = self.env['res.users'].sudo().search(['|', ('groups_id.name', '=', 'Show Full Accounting Features'), ('groups_id.name', '=', 'Mostrare funzionalità contabili complete')])
            user_counter += len(users)
            convt_date = datetime.strptime(obj_license['expiry_date'], '%Y-%m-%d')
            if datetime.now() > convt_date:
                raise odoo.exceptions.AccessDenied('Accesso non autorizzato per licenza scaduta')
        if user_counter > MAX_USERS:
            raise odoo.exceptions.AccessDenied('Numero massimo di utenti raggiunti, aggiungere una nuova licenza per continuare')


    # def decrypt_license(self, encrypted):
    #     # path = os.path.dirname(os.path.abspath(__file__))
    #     # path_join = os.path.normpath(os.path.join(path, '..', 'private_key.pem'))
    #     # with open(path_join, "rb") as key_file:
    #     private_key = serialization.load_pem_private_key(
    #         str.encode(io.StringIO(PRIVATE_KEY).read()),
    #         password=None,
    #         backend=default_backend()
    #     )
    #     #encrypted = bytes.fromhex(vals['license_key'])
    #     decrypted = private_key.decrypt(
    #         encrypted,
    #         padding.OAEP(
    #             mgf=padding.MGF1(algorithm=hashes.SHA256()),
    #             algorithm=hashes.SHA256(),
    #             label=None
    #         )
    #     )
    #     return decrypted
