# import json
# from . import app, client, create_token, db_reset, cache

# class TestActivity():
#     # Activity (Case 1 : Today)
#     def test_activity_case_1(self, client):
#         # Prepare the DB and token
#         db_reset()
#         token = create_token('budisetiawan')

#         data = {
#             'order_code': '',
#             'date': 'Hari Ini'
#         }

#         # Test the endpoints
#         res = client.get('/activity/1?order_code=' + data['order_code'] + '&date=' + data['date'], headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 200
    
#     # Activity (Case 2 : Yesterday)
#     def test_activity_case_2(self, client):
#         # Prepare the DB and token
#         token = create_token('hedy@alterra.id')

#         data = {
#             'order_code': '',
#             'date': 'Kemarin'
#         }

#         # Test the endpoints
#         res = client.get('/activity/1?order_code=' + data['order_code'] + '&date=' + data['date'], headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 200
    
#     # Activity (Case 3 : Using order code filter)
#     def test_activity_case_3(self, client):
#         # Prepare the DB and token
#         token = create_token('budisetiawan')

#         data = {
#             'order_code': 'A32BC1',
#             'date': 'Hari Ini'
#         }

#         # Test the endpoints
#         res = client.get('/activity/1?order_code=' + data['order_code'] + '&date=' + data['date'], headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 200

#     # Activity (Case 4 : Using order code filter Yesterday)
#     def test_activity_case_4(self, client):
#         # Prepare the DB and token
#         token = create_token('hedy@alterra.id')

#         data = {
#             'order_code': 'A32BC1',
#             'date': 'Kemarin'
#         }

#         # Test the endpoints
#         res = client.get('/activity/1?order_code=' + data['order_code'] + '&date=' + data['date'], headers={'Authorization': 'Bearer ' + token})
#         res_json = json.loads(res.data)
#         assert res.status_code == 200
    
#     # testing option
#     def test_option(self, client):
#         # Test the endpoints
#         res = client.options('/activity/1')
#         assert res.status_code == 200