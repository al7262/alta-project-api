# import json
# from . import app, client, create_token, db_reset, cache

# class TestEmployee():
#     # testing create employee valid
#     def test_create_employee_valid(self, client):
#         # get token 
#         token = create_token('hedy@alterra.id')
#         # Prepare the DB
#         db_reset()

#         # Prepare the data to be inputted
#         data = {
#             "id_outlet": 1,
#             "full_name": "Hedy Gading",
#             "username": "Hedy",
#             "password": "Gading09",
#             "position": "Admin"
#         }

#         # Test the endpoints
#         res = client.post('/employee/create', json = data, headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 200
#         assert res_json['message'] == 'Input Pegawai Berhasil'

#     # testing create employee invalid (input is not full)
#     def test_create_employee_invalid_input(self, client):
#         # get token 
#         token = create_token('hedy@alterra.id')
#         # Prepare the DB
#         db_reset()

#         # Prepare the data to be inputted
#         data = {
#             "id_outlet": 1,
#             "full_name": "Hedy Gading",
#             "username": "Hedy",
#             "password": "",
#             "position": "Admin"
#         }

#         # Test the endpoints
#         res = client.post('/employee/create', json = data, headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 400
#         assert res_json['message'] == 'tidak boleh ada kolom yang dikosongkan'

#     # testing create employee invalid (invalid password validation)
#     def test_create_employee_invalid_password_validation(self, client):
#         # get token 
#         token = create_token('hedy@alterra.id')
#         # Prepare the DB
#         db_reset()

#         # Prepare the data to be inputted
#         data = {
#             "id_outlet": 1,
#             "full_name": "Hedy Gading",
#             "username": "Hedy",
#             "password": "gading09",
#             "position": "Admin"
#         }

#         # Test the endpoints
#         res = client.post('/employee/create', json = data, headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 422

#     # testing create employee invalid (username already exists)
#     def test_create_employee_invalid_username_already_exists(self, client):
#         # get token 
#         token = create_token('hedy@alterra.id')
#         # Prepare the DB
#         db_reset()

#         # Prepare the data to be inputted
#         data = {
#             "id_outlet": 1,
#             "full_name": "Budi Setiawan",
#             "username": "budisetiawan",
#             "password": "gading09",
#             "position": "Admin"
#         }

#         # Test the endpoints
#         res = client.post('/employee/create', json = data, headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 401
    
#     # testing display employee data valid (no outlet params)
#     def test_employee_data_valid_empty_params_outlet(self, client):
#         # get token 
#         token = create_token('hedy@alterra.id')
#         # Prepare the DB
#         db_reset()

#         # Test the endpoints
#         res = client.get('/employee?position=Kasir', headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 200
    
#     # testing display employee data valid (no params)
#     def test_employee_data_valid_empty_all_params(self, client):
#         # get token 
#         token = create_token('hedy@alterra.id')
#         # Prepare the DB
#         db_reset()

#         # Test the endpoints
#         res = client.get('/employee', headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 200
    
#     # testing display employee data invalid (not fount)
#     def test_employee_data_invalid(self, client):
#         # get token 
#         token = create_token('hedy@alterra.id')
#         # Prepare the DB
#         db_reset()

#         # Test the endpoints
#         res = client.delete('/outlet/1', headers={'Authorization': 'Bearer ' + token})
#         res = client.get('/employee?name_outlet=Surabaya', headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 404
#         db_reset()

#     # testing display employee data valid (name_outlet, keyword)
#     def test_employee_data_valid_outlet_keyword(self, client):
#         # get token 
#         token = create_token('hedy@alterra.id')
#         # Prepare the DB
#         db_reset()

#         # Test the endpoints
#         res = client.get('/employee?name_outlet=Surabaya&keyword=budi', headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 200

#     # testing display employee data valid (name_outlet,position, keyword)
#     def test_employee_data_valid_outlet_position_keyword(self, client):
#         # get token 
#         token = create_token('hedy@alterra.id')
#         # Prepare the DB
#         db_reset()

#         # Test the endpoints
#         res = client.get('/employee?name_outlet=Surabaya&keyword=budi&position=Kasir', headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 200
    
#     # testing display employee data valid (keyword)
#     def test_employee_data_valid_keyword(self, client):
#         # get token 
#         token = create_token('hedy@alterra.id')
#         # Prepare the DB
#         db_reset()

#         # Test the endpoints
#         res = client.get('/employee?keyword=budi', headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 200

#     # testing display employee data valid (position, keyword)
#     def test_employee_data_valid_position_keyword(self, client):
#         # get token 
#         token = create_token('hedy@alterra.id')
#         # Prepare the DB
#         db_reset()

#         # Test the endpoints
#         res = client.get('/employee?position=Kasir&keyword=budi', headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 200

#     # testing display employee data valid (outlet, position)
#     def test_employee_data_valid_outlet_position(self, client):
#         # get token 
#         token = create_token('hedy@alterra.id')
#         # Prepare the DB
#         db_reset()

#         # Test the endpoints
#         res = client.get('/employee?name_outlet=Surabaya&position=Kasir', headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 200

#     # testing display employee data valid (outlet)
#     def test_employee_data_valid_outlet(self, client):
#         # get token 
#         token = create_token('hedy@alterra.id')
#         # Prepare the DB
#         db_reset()

#         # Test the endpoints
#         res = client.get('/employee?name_outlet=Surabaya', headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 200

#     # testing edit employee data valid (full params)
#     def test_edit_employee_data_valid(self, client):
#         # get token 
#         token = create_token('hedy@alterra.id')
#         # Prepare the DB
#         db_reset()

#         # Prepare the data to be inputted
#         data = {
#             "id_outlet": 1,
#             "fullname": "Budi Setiawan",
#             "username": "budisetiawan",
#             "password": "Gading09",
#             "position": "Admin"
#         }

#         # Test the endpoints
#         res = client.put('/employee/1', json = data, headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 200

#     # testing edit employee data invalid (wrong password)
#     def test_edit_employee_data_invalid_password(self, client):
#         # get token 
#         token = create_token('hedy@alterra.id')
#         # Prepare the DB
#         db_reset()

#         # Prepare the data to be inputted
#         data = {
#             "id_outlet": 1,
#             "fullname": "Budi Setiawan",
#             "username": "budisetiawan",
#             "password": "gading09",
#             "position": "Admin"
#         }

#         # Test the endpoints
#         res = client.put('/employee/1', json = data, headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 422

#     # testing delete employee data valid
#     def test_delete_employee_data_valid(self, client):
#         # get token 
#         token = create_token('hedy@alterra.id')
#         # Prepare the DB
#         db_reset()

#         # res = client.delete('/outlet/1', headers={'Authorization': 'Bearer ' + token})
        
#         # Test the endpoints
#         res = client.delete('/employee/1', headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 200
#         db_reset()

#     # testing delete employee data invalid
#     def test_delete_employee_data_invalid(self, client):
#         # get token 
#         token = create_token('hedy@alterra.id')
#         # Prepare the DB
#         db_reset()

#         res = client.delete('/employee/1', headers={'Authorization': 'Bearer ' + token})
        
#         # Test the endpoints
#         res = client.delete('/employee/1', headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 404
#         db_reset()

#     # testing display employee data by one valid
#     def test_delete_employee_data_by_one_valid(self, client):
#         # get token 
#         token = create_token('hedy@alterra.id')
#         # Prepare the DB
#         db_reset()
       
#         # Test the endpoints
#         res = client.get('/employee/get/1', headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 200
    
#     # testing display employee data by one invalid
#     def test_delete_employee_data_by_one_invalid(self, client):
#         # get token 
#         token = create_token('hedy@alterra.id')
#         # Prepare the DB
#         db_reset()
       
#         # Test the endpoints
#         res = client.get('/employee/get/12', headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 404