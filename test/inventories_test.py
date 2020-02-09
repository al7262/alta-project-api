# import json
# from . import app, client, create_token, db_reset, cache

# class TestInventories():
#         # Add new inventory (Case 1 : Empty field)
#     def test_add_new_inventory_case_1(self, client):
#         # Prepare the DB and token
#         token = create_token('stevejobs')

#         data = {
#             'name': '',
#             'stock': 2000,
#             'unit': 'gram',
#             'unit_price': 10,
#             'reminder': 500
#         }

#         # Test the endpoints
#         res = client.post('/inventory/1', json = data, headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 400
    
#     # Add new inventory (Case 2 : Positivity constraint 1)
#     def test_add_new_inventory_case_2(self, client):
#         # Prepare the DB and token
#         token = create_token('stevejobs')

#         data = {
#             'name': '',
#             'stock': -1,
#             'unit': 'gram',
#             'unit_price': 10,
#             'reminder': 500
#         }

#         # Test the endpoints
#         res = client.post('/inventory/1', json = data, headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 400

#     # Add new inventory (Case 3 : Positivity constraint 2)
#     def test_add_new_inventory_case_3(self, client):
#         # Prepare the DB and token
#         token = create_token('stevejobs')

#         data = {
#             'name': '',
#             'stock': 2000,
#             'unit': 'gram',
#             'unit_price': -1,
#             'reminder': 500
#         }

#         # Test the endpoints
#         res = client.post('/inventory/1', json = data, headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 400

#     # Add new inventory (Case 4 : Positivity constraint 3)
#     def test_add_new_inventory_case_4(self, client):
#         # Prepare the DB and token
#         token = create_token('hedy@alterra.id')

#         data = {
#             'name': '',
#             'stock': 2000,
#             'unit': 'gram',
#             'unit_price': 10,
#             'reminder': -1
#         }

#         # Test the endpoints
#         res = client.post('/inventory/1', json = data, headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 400
    
#     # Add new inventory (Case 5 : Add new inventory)
#     def test_add_new_inventory_case_5(self, client):
#         # Prepare the DB and token
#         token = create_token('hedy@alterra.id')

#         data = {
#             'name': 'Cabe Keriting',
#             'stock': 2000,
#             'unit': 'gram',
#             'unit_price': 10,
#             'reminder': 300
#         }

#         # Test the endpoints
#         res = client.post('/inventory/1', json = data, headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 200
    
#     # Add new inventory (Case 6 : Duplicate inventory)
#     def test_add_new_inventory_case_6(self, client):
#         # Prepare the DB and token
#         token = create_token('hedy@alterra.id')

#         data = {
#             'name': 'Cabe Keriting',
#             'stock': 2000,
#             'unit': 'gram',
#             'unit_price': 10,
#             'reminder': 300
#         }

#         # Test the endpoints
#         res = client.post('/inventory/1', json = data, headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 409

#     # Add new inventory (Case 7 : Inventory exist but unit is wrong)
#     def test_add_new_inventory_case_7(self, client):
#         # Prepare the DB and token
#         token = create_token('hedy@alterra.id')

#         data = {
#             'name': 'Cabe Keriting',
#             'stock': 2000,
#             'unit': 'pcs',
#             'unit_price': 10,
#             'reminder': 300
#         }

#         # Test the endpoints
#         res = client.post('/inventory/1', json = data, headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 409
    
#     # Add new inventory (Case 8 : Add same inventory in different outlet)
#     def test_add_new_inventory_case_8(self, client):
#         # Prepare the DB and token
#         token = create_token('hedy@alterra.id')

#         data = {
#             'name': 'Cabe Keriting',
#             'stock': 2000,
#             'unit': 'gram',
#             'unit_price': 10,
#             'reminder': 300
#         }

#         # Test the endpoints
#         res = client.post('/inventory/2', json = data, headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 200

#     # Add new inventory (Case 9 : Add inventory below reminder)
#     def test_add_new_inventory_case_9(self, client):
#         # Prepare the DB and token
#         token = create_token('stevejobs')

#         data = {
#             'name': 'Paprika',
#             'stock': 2000,
#             'unit': 'gram',
#             'unit_price': 23,
#             'reminder': 3000
#         }

#         # Test the endpoints
#         res = client.post('/inventory/1', json = data, headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 200

#     # Get all inventories (Case 1 : Not found by name filter)
#     def test_get_all_inventories_case_1(self, client):
#         # Prepare the DB and token
#         token = create_token('stevejobs')

#         data = {
#             'status': '',
#             'name': 'Mie Gaga'
#         }

#         # Test the endpoints
#         res = client.get('/inventory?status=' + data['status'] + '&name=' + data['name'], headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 200

#     # Get all inventories (Case 2 : Filter status tersedia)
#     def test_get_all_inventories_case_2(self, client):
#         # Prepare the DB and token
#         token = create_token('hedy@alterra.id')

#         data = {
#             'status': 'Tersedia',
#             'name': ''
#         }

#         # Test the endpoints
#         res = client.get('/inventory?status=' + data['status'] + '&name=' + data['name'], headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 200
    
#     # Get all inventories (Case 3 : Filter status hampir habis)
#     def test_get_all_inventories_case_3(self, client):
#         # Prepare the DB and token
#         token = create_token('hedy@alterra.id')

#         data = {
#             'status': 'Hampir Habis',
#             'name': ''
#         }

#         # Test the endpoints
#         res = client.get('/inventory?status=' + data['status'] + '&name=' + data['name'], headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 200
    
#     # Get all inventories in an outlet (Case 1 : Not found by name filter)
#     def test_get_all_inventories_outlet_case_1(self, client):
#         # Prepare the DB and token
#         token = create_token('stevejobs')

#         data = {
#             'status': '',
#             'name': 'Mie Gaga'
#         }

#         # Test the endpoints
#         res = client.get('/inventory/1?status=' + data['status'] + '&name=' + data['name'], headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 200

#     # Get all inventories (Case 2 : Filter status tersedia)
#     def test_get_all_inventories_outlet_case_2(self, client):
#         # Prepare the DB and token
#         token = create_token('hedy@alterra.id')

#         data = {
#             'status': 'Tersedia',
#             'name': ''
#         }

#         # Test the endpoints
#         res = client.get('/inventory/1?status=' + data['status'] + '&name=' + data['name'], headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 200
    
#     # Get all inventories (Case 3 : Filter status hampir habis)
#     def test_get_all_inventories_outlet_case_3(self, client):
#         # Prepare the DB and token
#         token = create_token('hedy@alterra.id')

#         data = {
#             'status': 'Hampir Habis',
#             'name': ''
#         }

#         # Test the endpoints
#         res = client.get('/inventory/1?status=' + data['status'] + '&name=' + data['name'], headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 200
    
#     # Get specific inventory by ID    
#     def test_get_inventory_by_id(self, client):
#         # Prepare the DB and token
#         token = create_token('hedy@alterra.id')

#         # Test the endpoints
#         res = client.get('/inventory/detail/1', headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 200

#     # Edit stock outlet (Case 1 : Empty field)
#     def test_edit_stock_outlet_case_1(self, client):
#         # Prepare the DB and token
#         token = create_token('hedy@alterra.id')

#         data = {
#             'name': '',
#             'stock': 25,
#             'unit': 'butir',
#             'reminder': 10
#         }

#         # Test the endpoints
#         res = client.put('/inventory/detail/1', json = data, headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 400
    
#     # Edit stock outlet (Case 2 : Positivity constraint 1)
#     def test_edit_stock_outlet_case_2(self, client):
#         # Prepare the DB and token
#         token = create_token('hedy@alterra.id')

#         data = {
#             'name': 'Telur',
#             'stock': 25,
#             'unit': 'butir',
#             'reminder': -1
#         }

#         # Test the endpoints
#         res = client.put('/inventory/detail/1', json = data, headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 400
    
#     # Edit stock outlet (Case 3 : Positivity constraint 2)
#     def test_edit_stock_outlet_case_3(self, client):
#         # Prepare the DB and token
#         token = create_token('hedy@alterra.id')

#         data = {
#             'name': 'Telur',
#             'stock': -1,
#             'unit': 'butir',
#             'reminder': 5
#         }

#         # Test the endpoints
#         res = client.put('/inventory/detail/1', json = data, headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 400

#     # Edit stock outlet (Case 4 : success)
#     def test_edit_stock_outlet_case_4(self, client):
#         # Prepare the DB and token
#         token = create_token('hedy@alterra.id')

#         data = {
#             'name': 'Telur',
#             'stock': 10,
#             'unit': 'butir',
#             'reminder': 5
#         }

#         # Test the endpoints
#         res = client.put('/inventory/detail/1', json = data, headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 200
    
#     # Soft delete inventory
#     def test_soft_delete_inventory(self, client):
#         # Prepare the DB and token
#         token = create_token('hedy@alterra.id')

#         # Test the endpoints
#         res = client.delete('/inventory/detail/2', headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 200
    
#     # Add stock to an inventory (Case 1: Empty field)
#     def test_add_stock_case_1(self, client):
#         # Prepare the DB and token
#         token = create_token('hedy@alterra.id')

#         data = {
#             'stock': "",
#             'price': 25000
#         }   

#         # Test the endpoints
#         res = client.put('/inventory/add-stock/1', json = data, headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 400

#     # Add stock to an inventory (Case 2: Positivity constraint 1)
#     def test_add_stock_case_2(self, client):
#         # Prepare the DB and token
#         token = create_token('hedy@alterra.id')

#         data = {
#             'stock': -1,
#             'price': 25000
#         }   

#         # Test the endpoints
#         res = client.put('/inventory/add-stock/1', json = data, headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 400

#     # Add stock to an inventory (Case 3: Positivity constraint 2)
#     def test_add_stock_case_3(self, client):
#         # Prepare the DB and token
#         token = create_token('hedy@alterra.id')

#         data = {
#             'stock': 20,
#             'price': -25000
#         }   

#         # Test the endpoints
#         res = client.put('/inventory/add-stock/1', json = data, headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 400

#     # Add stock to an inventory (Case 4: Success)
#     def test_add_stock_case_4(self, client):
#         # Prepare the DB and token
#         token = create_token('stevejobs')

#         data = {
#             'stock': 20,
#             'price': 30000
#         }   

#         # Test the endpoints
#         res = client.put('/inventory/add-stock/1', json = data, headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 200

#     # Stock reminder in an outlet
#     def test_stock_reminder_outlet(self, client):
#         # Prepare the DB and token
#         token = create_token('stevejobs')

#         # Test the endpoints
#         res = client.get('/inventory/reminder/1', headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 200
    
#     # Stock reminder in all outlets
#     def test_stock_reminder_all_outlets(self, client):
#         # Prepare the DB and token
#         token = create_token('hedy@alterra.id')

#         # Test the endpoints
#         res = client.get('/inventory/reminder', headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 200