import json
from . import app, client, create_token, db_reset, cache

class TestCustomers():
    # Get all customers (Case 1: Missing keyword parameter)
    def test_get_all_customers_case_1(self, client):
        db_reset()
        # Prepare the DB and token
        token = create_token('stevejobs')

        # Test the endpoints
        res = client.get('/customer', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # Get all customers (Case 2: Using keyword parameter)
    def test_get_all_customers_case_2(self, client):
        # Prepare the DB and token
        token = create_token('hedy@alterra.id')

        # Test the endpoints
        res = client.get('/customer?keyword=Leli', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    # Edit customer (Case 1: Empty name field)
    def test_edit_customer_case_1(self, client):
        # Prepare the DB and token
        token = create_token('budisetiawan')

        data = {
            'fullname': '',
            'phone_number': '089512345678',
            'email': ''
        }

        # Test the endpoints
        res = client.put('/customer/1', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 400
    
    # Edit customer (Case 2: Success edit customer)
    def test_edit_customer_case_2(self, client):
        # Prepare the DB and token
        token = create_token('hedy@alterra.id')

        data = {
            'fullname': 'Lelianto',
            'phone_number': '089512345678',
            'email': 'lelianto@alterra.id'
        }

        # Test the endpoints
        res = client.put('/customer/1', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # Add customer (Case 1: Empty name field)
    def test_add_customer_case_1(self, client):
        # Prepare the DB and token
        token = create_token('budisetiawan')

        data = {
            'fullname': '',
            'phone_number': '089512345678',
            'email': ''
        }

        # Test the endpoints
        res = client.post('/customer/create', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 400

    # Add customer (Case 2: Success)
    def test_add_customer_case_2(self, client):
        # Prepare the DB and token
        token = create_token('hedy@alterra.id')

        data = {
            'fullname': 'Joni English',
            'phone_number': '089512345679',
            'email': ''
        }

        # Test the endpoints
        res = client.post('/customer/create', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    # Add customer (Case 3: Failed)
    def test_add_customer_case_3(self, client):
        # Prepare the DB and token
        token = create_token('hedy@alterra.id')

        data = {
            'fullname': 'Joni English',
            'phone_number': '089512345679',
            'email': ''
        }

        # Test the endpoints
        res = client.post('/customer/create', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 409

    # Get customer by ID success
    def test_get_customer_by_id_success(self, client):
        # Prepare the DB and token
        token = create_token('hedy@alterra.id')

        # Test the endpoints
        res = client.get('/customer/get/1', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    # Get customer by ID failed
    def test_get_customer_by_id_failed(self, client):
        # Prepare the DB and token
        token = create_token('budisetiawan')

        # Test the endpoints
        res = client.get('/customer/get/1917', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 404
    
    # testing option
    def test_option(self, client):
        # Test the endpoints
        res = client.options('/customer')
        res = client.options('/customer/create')
        res = client.options('/customer/get/1')
        assert res.status_code == 200
    
    # Delete customer
    def test_delete_customer_by_id(self, client):
        # Prepare the DB and token
        token = create_token('budisetiawan')

        cart = {
            'id_outlet': 1,
            'id_customers': 1,
            'item_list': [
                {'id': 1, 'unit': 2, 'price': 12000},
                {'id': 2, 'unit': 1, 'price': 16000},
                {'id': 3, 'unit': 3, 'price': 15000}
            ],
            'promo': '',
            'payment_method': 'Tunai',
            'paid_price': 100000,
            'name': 'Lelianto Eko Pradana',
            'phone': '',
            'email': ''
        }

        # Test the endpoints
        res = client.post('/product/checkout', json = cart, headers={'Authorization': 'Bearer ' + token})
        res = client.post('/product/checkout', json = cart, headers={'Authorization': 'Bearer ' + token})
        res = client.delete('/customer/1', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # Get loyal customer
    def test_loyal_customer(self, client):
        # Prepare the DB and token
        token = create_token('budisetiawan')

        cart = {
            'id_outlet': 1,
            'id_customers': 1,
            'item_list': [
                {'id': 1, 'unit': 2, 'price': 12000},
                {'id': 2, 'unit': 1, 'price': 16000},
                {'id': 3, 'unit': 3, 'price': 15000}
            ],
            'promo': '',
            'payment_method': 'Tunai',
            'paid_price': 100000,
            'name': 'Lelianto Eko Pradana',
            'phone': '',
            'email': ''
        }

        # Test the endpoints
        res = client.post('/product/checkout', json = cart, headers={'Authorization': 'Bearer ' + token})
        res = client.post('/product/checkout', json = cart, headers={'Authorization': 'Bearer ' + token})
        res = client.get('/customer', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200