import xmlrpc.client

url = 'http://localhost:8069'
db = 'construction_erp'
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

# Find stages
stages = models.execute_kw(db, uid, password, 'crm.stage', 'search_read', [[], ['name']])
stage_map = {s['name']: s['id'] for s in stages}

initial_stage_id = stage_map.get('Initial Discussion')
visit_stage_id = stage_map.get('Site Visit Scheduled')

# Create Lead
lead_id = models.execute_kw(db, uid, password, 'crm.lead', 'create', [{
    'name': 'Test Validation Lead',
    'stage_id': initial_stage_id
}])

print("Lead created.")

# Try to move without date
try:
    models.execute_kw(db, uid, password, 'crm.lead', 'write', [[lead_id], {'stage_id': visit_stage_id}])
    print("FAILED: Did not raise validation error!")
except Exception as e:
    if "Please enter date" in str(e):
        print("SUCCESS: Validation error raised correctly.")
    else:
        print(f"FAILED: Wrong error message or other error: {e}")

# Try to move with date
try:
    models.execute_kw(db, uid, password, 'crm.lead', 'write', [[lead_id], {
        'stage_id': visit_stage_id,
        'site_visit_date': '2026-03-30'
    }])
    print("SUCCESS: Lead moved successfully with date.")
except Exception as e:
    print(f"FAILED: Could not move with date. Error: {e}")
