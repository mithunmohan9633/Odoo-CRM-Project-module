import xmlrpc.client

url = 'http://localhost:8069'
db = 'construction_erp'
username = 'admin'
password = 'admin'

def upgrade_module():
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
    uid = common.authenticate(db, username, password, {})
    
    # Update app list
    models.execute_kw(db, uid, password, 'ir.module.module', 'update_list', [[]])
    
    module_ids = models.execute_kw(db, uid, password, 'ir.module.module', 'search', [[('name', '=', 'construction_workflow')]])
    if module_ids:
        print(f"Upgrading module_ids: {module_ids}")
        models.execute_kw(db, uid, password, 'ir.module.module', 'button_immediate_upgrade', [module_ids])
        print("Successfully upgraded construction_workflow!")
    else:
        print("Module not found!")

if __name__ == "__main__":
    upgrade_module()
