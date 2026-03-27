import xmlrpc.client

url = 'http://localhost:8069'
db = 'construction_erp'
username = 'admin'
password = 'admin'

def cleanup():
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
    uid = common.authenticate(db, username, password, {})
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

    # Delete all leads to free up stages
    lead_ids = models.execute_kw(db, uid, password, 'crm.lead', 'search', [[]])
    if lead_ids:
        models.execute_kw(db, uid, password, 'crm.lead', 'unlink', [lead_ids])

    # Delete default stages
    default_names = ['New', 'Qualified', 'Proposition']
    stage_ids = models.execute_kw(db, uid, password, 'crm.stage', 'search', [[('name', 'in', default_names)]])
    if stage_ids:
        models.execute_kw(db, uid, password, 'crm.stage', 'unlink', [stage_ids])
    
    # Let's ensure there are no duplicate "Won"
    won_ids = models.execute_kw(db, uid, password, 'crm.stage', 'search', [[('name', '=', 'Won')]])
    if len(won_ids) > 1:
        # Keep the one with highest ID (the newest), delete rest
        models.execute_kw(db, uid, password, 'crm.stage', 'unlink', [won_ids[:-1]])

    print("Cleanup successful.")

if __name__ == "__main__":
    cleanup()
