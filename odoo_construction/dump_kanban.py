import xmlrpc.client

url = 'http://localhost:8069'
db = 'construction_erp'
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

ir_model_data = models.execute_kw(db, uid, password, 'ir.model.data', 'search_read', [[('module', '=', 'crm'), ('name', '=', 'crm_case_kanban_view_leads')], ['res_id']])
if ir_model_data:
    view_id = ir_model_data[0]['res_id']
    base_view = models.execute_kw(db, uid, password, 'ir.ui.view', 'read', [[view_id], ['arch']])
    with open('kanban_arch.xml', 'w') as f:
        f.write(base_view[0]['arch'])
    print("Kanban dumped")
else:
    print("Kanban view not found")
