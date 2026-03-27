import xmlrpc.client

url = 'http://localhost:8069'
db = 'construction_erp'
username = 'admin'
password = 'admin'

def setup_all():
    try:
        common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
        uid = common.authenticate(db, username, password, {})
        if not uid:
            print("Authentication failed.")
            return

        models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

        # Deactivate existing stages
        stage_ids = models.execute_kw(db, uid, password, 'crm.stage', 'search', [[]])
        if stage_ids:
            try:
                models.execute_kw(db, uid, password, 'crm.stage', 'unlink', [stage_ids])
            except Exception as e:
                print(f"Could not unlink stages, error: {e}")

        # Create new stages
        stages = [
            {'name': 'Initial Discussion', 'sequence': 1, 'is_won': False},
            {'name': 'Site Visit Scheduled', 'sequence': 2, 'is_won': False},
            {'name': 'Site Visit Completed', 'sequence': 3, 'is_won': False},
            {'name': 'Concept Plan Preparation', 'sequence': 4, 'is_won': False},
            {'name': 'BOQ / Cost Estimation', 'sequence': 5, 'is_won': False},
            {'name': 'Quotation Submitted', 'sequence': 6, 'is_won': False},
            {'name': 'Won', 'sequence': 7, 'is_won': True},
        ]

        for s in stages:
            models.execute_kw(db, uid, password, 'crm.stage', 'create', [s])

        print("Successfully updated CRM stages!")
        
        # Now lost reasons
        lost_reasons = [
            {'name': 'Too Expensive'},
            {'name': 'Chose Competitor'},
            {'name': 'Project Cancelled'},
            {'name': 'Not Enough Resources'},
            {'name': 'Poor Requirements'}
        ]
        
        existing_reasons = models.execute_kw(db, uid, password, 'crm.lost.reason', 'search_read', [[], ['name']])
        existing_names = [r['name'] for r in existing_reasons]
        
        for lr in lost_reasons:
            if lr['name'] not in existing_names:
                models.execute_kw(db, uid, password, 'crm.lost.reason', 'create', [lr])
                
        print("Successfully updated Lost Reasons!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    setup_all()
