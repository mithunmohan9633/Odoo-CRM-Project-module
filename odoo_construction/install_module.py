import xmlrpc.client

url = 'http://localhost:8069'
db = 'construction_erp'
username = 'admin'
password = 'admin'

def install_module():
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

    # Update app list
    models.execute_kw(db, uid, password, 'ir.module.module', 'update_list', [[]])

    # Search for our custom module
    module_ids = models.execute_kw(db, uid, password, 'ir.module.module', 'search', [[('name', '=', 'construction_workflow')]])
    if module_ids:
        print(f"Installing module_ids: {module_ids}")
        models.execute_kw(db, uid, password, 'ir.module.module', 'button_immediate_install', [module_ids])
        print("Successfully installed construction_workflow!")
    else:
        print("Module not found!")

if __name__ == "__main__":
    install_module()
