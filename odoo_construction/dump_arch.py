import xmlrpc.client

url = 'http://localhost:8069'
db = 'construction_erp'
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

base_view = models.execute_kw(db, uid, password, 'ir.ui.view', 'read', [[604], ['arch']])
with open('base_arch.xml', 'w') as f:
    f.write(base_view[0]['arch'])
