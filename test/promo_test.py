# import json
# from . import app, client, create_token, db_reset, cache

# class TestPromo():
#     # testing display promo valid (with keyword)
#     def test_display_promo_valid(self, client):
#         # get token 
#         token = create_token('hedy@alterra.id')
#         # Prepare the DB
#         db_reset()

#         # Test the endpoints
#         res = client.get('/promo?keyword=', headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 200

#     # testing display promo valid (no keyword)
#     def test_display_promo_valid_no_keyword(self, client):
#         # get token 
#         token = create_token('hedy@alterra.id')
#         # Prepare the DB
#         db_reset()

#         # Test the endpoints
#         res = client.get('/promo', headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 200

#     # testing delete promo valid
#     def test_delete_promo_valid(self, client):
#         # get token 
#         token = create_token('hedy@alterra.id')
#         # Prepare the DB
#         db_reset()

#         # Test the endpoints
#         res = client.delete('/promo/1', headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 200
    
#     # testing delete promo invalid
#     def test_delete_promo_invalid(self, client):
#         # get token 
#         token = create_token('hedy@alterra.id')
#         # Prepare the DB
#         db_reset()

#         # Test the endpoints
#         res = client.delete('/promo/1', headers={'Authorization': 'Bearer ' + token})
#         res = client.delete('/promo/1', headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 404
    
#     # testing delete promo invalid
#     def test_delete_promo_invalid(self, client):
#         # get token 
#         token = create_token('hedy@alterra.id')
#         # Prepare the DB
#         db_reset()

#         # Test the endpoints
#         res = client.delete('/promo/1', headers={'Authorization': 'Bearer ' + token})
#         res = client.delete('/promo/1', headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 404

#     # testing create promo valid
#     def test_create_promo_valid(self, client):
#         # get token 
#         token = create_token('hedy@alterra.id')
#         # Prepare the DB
#         db_reset()

#         # data input
#         data = {
#             "name": "Alterra Pesta",
#             "day": ["Senin","Selasa","Rabu"],
#             "discount": [10,10],
#             "product" : ["Indomie Yogyakarta","Indomie Ayam Geprek"]
#         }

#         # Test the endpoints
#         res = client.post('/promo/create', json = data, headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 200
    
#     # testing create promo invalid
#     def test_create_promo_invalid(self, client):
#         # get token 
#         token = create_token('hedy@alterra.id')
#         # Prepare the DB
#         db_reset()

#         # data input
#         data = {
#             "name": "Alterra Pesta",
#             "day": ["Senin","Selasa","Rabu"],
#             "discount": [10,10],
#             "product" : ["Indomie Yogyakarta","Indomie Ayam Geprek"]
#         }

#         # Test the endpoints
#         res = client.post('/promo/create', json = data, headers={'Authorization': 'Bearer ' + token})
#         res = client.post('/promo/create', json = data, headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 409

#     # testing display by one promo valid
#     def test_display_promo_valid_by_one(self, client):
#         # get token 
#         token = create_token('hedy@alterra.id')
#         # Prepare the DB
#         db_reset()

#         # Test the endpoints
#         res = client.get('/promo/get/1', headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 200

#     # testing display by one promo invalid
#     def test_display_promo_invalid_by_one(self, client):
#         # get token 
#         token = create_token('hedy@alterra.id')
#         # Prepare the DB
#         db_reset()

#         # Test the endpoints
#         res = client.delete('/promo/1', headers={'Authorization': 'Bearer ' + token})
#         res = client.get('/promo/get/1', headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 404
    
#     # testing edit promo valid case 1
#     def test_edit_promo_valid_case_1(self, client):
#         # get token 
#         token = create_token('hedy@alterra.id')
#         # Prepare the DB
#         db_reset()

#         #input user
#         data = {
#             "name" : "Alterra Makan Makan",
#             "status" : False,
#             "day" : ["Senin", "Selasa"],
#             "product" : ["Indomie Yogyakarta","Indomie Ayam Geprek"],
#             "discount" : [5,5]
#         }

#         # Test the endpoints
#         res = client.put('/promo/1', json = data, headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 200
    
#     # testing edit promo valid case 2
#     def test_edit_promo_valid_case_2(self, client):
#         # get token 
#         token = create_token('hedy@alterra.id')
#         # Prepare the DB
#         db_reset()

#         #input user
#         data = {
#             "name" : "Alterra Makan Makan",
#             "status" : False,
#             "day" : ["Senin", "Selasa"],
#             "product" : ["Indomie Goreng","Indomie Ayam Geprek"],
#             "discount" : [5,5]
#         }

#         # Test the endpoints
#         res = client.put('/promo/1', json = data, headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 200

#     # testing edit promo invalid (not found)
#     def test_edit_promo_invalid_not_found(self, client):
#         # get token 
#         token = create_token('hedy@alterra.id')
#         # Prepare the DB
#         db_reset()

#         #input user
#         data = {
#             "name" : "Alterra Makan Makan",
#             "status" : False,
#             "day" : ["Senin", "Selasa"],
#             "product" : ["Indomie Yogyakarta","Indomie Ayam Geprek"],
#             "discount" : [5,5]
#         }

#         # Test the endpoints
#         res = client.delete('/promo/1', headers={'Authorization': 'Bearer ' + token})
#         res = client.put('/promo/1', json = data, headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 404