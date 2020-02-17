import json
from . import app, client, create_token, db_reset, cache

class TestReport():
    # Product Report (Case 1 - All filter without date)
    def test_product_report_case_1(self, client):
        # Prepare the DB and token
        db_reset()
        token = create_token('hedy@alterra.id')

        data = {
            'name': 'Indomie Goreng',
            'category': 'Indomie',
            'id_outlet': 1,
            'start_time': '',
            'end_time': '',
            'total_sold_sort': '',
            'total_sales_sort': ''
        }

        endpoint = '/report/product-sales'
        endpoint = endpoint + '?name=' + data['name']
        endpoint = endpoint + '&category=' + data['category']
        endpoint = endpoint + '&id_outlet=' + str(data['id_outlet'])
        endpoint = endpoint + '&start_time=' + data['start_time']
        endpoint = endpoint + '&end_time=' + data['end_time']
        endpoint = endpoint + '&total_sold_sort=' + data['total_sold_sort']
        endpoint = endpoint + '&total_sales_sort=' + data['total_sales_sort']

        # Test the endpoints
        res = client.get(endpoint, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    # Product Report (Case 3 - Filter by date)
    def test_product_report_case_3(self, client):
        # Prepare the DB and token
        db_reset()
        token = create_token('hedy@alterra.id')

        data = {
            'name': '',
            'category': '',
            'id_outlet': 1,
            'start_time': '01-01-2019',
            'end_time': '01-01-2099',
            'total_sold_sort': '',
            'total_sales_sort': ''
        }

        endpoint = '/report/product-sales'
        endpoint = endpoint + '?name=' + data['name']
        endpoint = endpoint + '&category=' + data['category']
        endpoint = endpoint + '&id_outlet=' + str(data['id_outlet'])
        endpoint = endpoint + '&start_time=' + data['start_time']
        endpoint = endpoint + '&end_time=' + data['end_time']
        endpoint = endpoint + '&total_sold_sort=' + data['total_sold_sort']
        endpoint = endpoint + '&total_sales_sort=' + data['total_sales_sort']

        # Test the endpoints
        res = client.get(endpoint, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    # Product Report (Case 4 - Sort 1)
    def test_product_report_case_4(self, client):
        # Prepare the DB and token
        db_reset()
        token = create_token('hedy@alterra.id')

        data = {
            'name': '',
            'category': '',
            'id_outlet': '',
            'start_time': '',
            'end_time': '',
            'total_sold_sort': 'asc',
            'total_sales_sort': 'desc'
        }

        endpoint = '/report/product-sales'
        endpoint = endpoint + '?name=' + data['name']
        endpoint = endpoint + '&category=' + data['category']
        endpoint = endpoint + '&id_outlet=' + str(data['id_outlet'])
        endpoint = endpoint + '&start_time=' + data['start_time']
        endpoint = endpoint + '&end_time=' + data['end_time']
        endpoint = endpoint + '&total_sold_sort=' + data['total_sold_sort']
        endpoint = endpoint + '&total_sales_sort=' + data['total_sales_sort']

        # Test the endpoints
        res = client.get(endpoint, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # Product Report (Case 5 - Sort 2)
    def test_product_report_case_5(self, client):
        # Prepare the DB and token
        db_reset()
        token = create_token('hedy@alterra.id')

        data = {
            'name': '',
            'category': '',
            'id_outlet': '',
            'start_time': '',
            'end_time': '',
            'total_sold_sort': 'desc',
            'total_sales_sort': 'asc'
        }

        endpoint = '/report/product-sales'
        endpoint = endpoint + '?name=' + data['name']
        endpoint = endpoint + '&category=' + data['category']
        endpoint = endpoint + '&id_outlet=' + str(data['id_outlet'])
        endpoint = endpoint + '&start_time=' + data['start_time']
        endpoint = endpoint + '&end_time=' + data['end_time']
        endpoint = endpoint + '&total_sold_sort=' + data['total_sold_sort']
        endpoint = endpoint + '&total_sales_sort=' + data['total_sales_sort']

        # Test the endpoints
        res = client.delete('/product/1', headers={'Authorization': 'Bearer ' + token})
        res = client.get(endpoint, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # History Report (Case 1 - No filter)
    def test_history_report_case_1(self, client):
        # Prepare the DB and token
        db_reset()
        token = create_token('hedy@alterra.id')

        data = {
            'name': '',
            'id_outlet': '',
            'start_time': '',
            'end_time': '',
            'total_sold_sort': '',
            'total_sales_sort': ''
        }

        endpoint = '/report/history'
        endpoint = endpoint + '?name=' + data['name']
        endpoint = endpoint + '&id_outlet=' + str(data['id_outlet'])
        endpoint = endpoint + '&start_time=' + data['start_time']
        endpoint = endpoint + '&end_time=' + data['end_time']
        endpoint = endpoint + '&total_sold_sort=' + data['total_sold_sort']
        endpoint = endpoint + '&total_sales_sort=' + data['total_sales_sort']

        # Test the endpoints
        res = client.get(endpoint, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # History Report (Case 2 - All filter without time)
    def test_history_report_case_2(self, client):
        # Prepare the DB and token
        db_reset()
        token = create_token('hedy@alterra.id')

        data = {
            'name': 'Indomie Goreng',
            'id_outlet': 1,
            'start_time': '',
            'end_time': '',
            'total_sold_sort': '',
            'total_sales_sort': ''
        }

        endpoint = '/report/history'
        endpoint = endpoint + '?name=' + data['name']
        endpoint = endpoint + '&id_outlet=' + str(data['id_outlet'])
        endpoint = endpoint + '&start_time=' + data['start_time']
        endpoint = endpoint + '&end_time=' + data['end_time']
        endpoint = endpoint + '&total_sold_sort=' + data['total_sold_sort']
        endpoint = endpoint + '&total_sales_sort=' + data['total_sales_sort']

        # Test the endpoints
        res = client.get(endpoint, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # History Report (Case 3 - Only filter time)
    def test_history_report_case_3(self, client):
        # Prepare the DB and token
        db_reset()
        token = create_token('hedy@alterra.id')

        data = {
            'name': '',
            'id_outlet': '',
            'start_time': '01-01-2019',
            'end_time': '01-01-2099',
            'total_sold_sort': '',
            'total_sales_sort': ''
        }

        endpoint = '/report/history'
        endpoint = endpoint + '?name=' + data['name']
        endpoint = endpoint + '&id_outlet=' + str(data['id_outlet'])
        endpoint = endpoint + '&start_time=' + data['start_time']
        endpoint = endpoint + '&end_time=' + data['end_time']
        endpoint = endpoint + '&total_sold_sort=' + data['total_sold_sort']
        endpoint = endpoint + '&total_sales_sort=' + data['total_sales_sort']

        # Test the endpoints
        res = client.get(endpoint, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # History Report (Case 4 - Sort 1)
    def test_history_report_case_4(self, client):
        # Prepare the DB and token
        db_reset()
        token = create_token('administrator03')

        data = {
            'name': '',
            'id_outlet': '',
            'start_time': '01-01-2019',
            'end_time': '01-01-2099',
            'total_sold_sort': 'asc',
            'total_sales_sort': 'desc'
        }

        endpoint = '/report/history'
        endpoint = endpoint + '?name=' + data['name']
        endpoint = endpoint + '&id_outlet=' + str(data['id_outlet'])
        endpoint = endpoint + '&start_time=' + data['start_time']
        endpoint = endpoint + '&end_time=' + data['end_time']
        endpoint = endpoint + '&total_sold_sort=' + data['total_sold_sort']
        endpoint = endpoint + '&total_sales_sort=' + data['total_sales_sort']

        # Test the endpoints
        res = client.get(endpoint, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # History Report (Case 5 - Sort 2)
    def test_history_report_case_5(self, client):
        # Prepare the DB and token
        db_reset()
        token = create_token('administrator02')

        data = {
            'name': '',
            'id_outlet': '',
            'start_time': '01-01-2019',
            'end_time': '01-01-2099',
            'total_sold_sort': 'desc',
            'total_sales_sort': 'asc'
        }

        endpoint = '/report/history'
        endpoint = endpoint + '?name=' + data['name']
        endpoint = endpoint + '&id_outlet=' + str(data['id_outlet'])
        endpoint = endpoint + '&start_time=' + data['start_time']
        endpoint = endpoint + '&end_time=' + data['end_time']
        endpoint = endpoint + '&total_sold_sort=' + data['total_sold_sort']
        endpoint = endpoint + '&total_sales_sort=' + data['total_sales_sort']

        # Test the endpoints
        res = client.get(endpoint, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # History Report (Case 6 - Sort 3)
    def test_history_report_case_6(self, client):
        # Prepare the DB and token
        db_reset()
        token = create_token('administrator04')

        data = {
            'name': '',
            'id_outlet': '',
            'start_time': '01-01-2019',
            'end_time': '01-01-2099',
            'total_sold_sort': 'desc',
            'total_sales_sort': ''
        }

        endpoint = '/report/history'
        endpoint = endpoint + '?name=' + data['name']
        endpoint = endpoint + '&id_outlet=' + str(data['id_outlet'])
        endpoint = endpoint + '&start_time=' + data['start_time']
        endpoint = endpoint + '&end_time=' + data['end_time']
        endpoint = endpoint + '&total_sold_sort=' + data['total_sold_sort']
        endpoint = endpoint + '&total_sales_sort=' + data['total_sales_sort']

        # Test the endpoints
        res = client.get(endpoint, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # Inventory Log (Case 1)
    def test_inventory_log_report_case_1(self, client):
        # Prepare the DB and token
        db_reset()
        token = create_token('hedy@alterra.id')

        data = {
            'name': 'mie',
            'id_outlet': '1',
            'type': 'Masuk',
            'start_time': '01-01-2019',
            'end_time': '01-01-2099',
            'amount_sort': 'desc',
        }

        endpoint = '/report/inventory-log'
        endpoint = endpoint + '?name=' + data['name']
        endpoint = endpoint + '&id_outlet=' + str(data['id_outlet'])
        endpoint = endpoint + '&type=' + data['type']
        endpoint = endpoint + '&start_time=' + data['start_time']
        endpoint = endpoint + '&end_time=' + data['end_time']
        endpoint = endpoint + '&amount_sort=' + data['amount_sort']

        data_1 = {
            'stock': 1000,
            'price': 15000
        }

        data_2 = {
            'stock': 1200,
            'price': 13000
        }

        data_3 = {
            'stock': 800,
            'price': 14000
        }

        # Test the endpoints
        res = client.put('/inventory/add-stock/1', json = data_1, headers={'Authorization': 'Bearer ' + token})
        res = client.put('/inventory/add-stock/2', json = data_2, headers={'Authorization': 'Bearer ' + token})
        res = client.put('/inventory/add-stock/3', json = data_3, headers={'Authorization': 'Bearer ' + token})
        res = client.get(endpoint, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # Inventory Log (Case 2)
    def test_inventory_log_report_case_2(self, client):
        # Prepare the DB and token
        db_reset()
        token = create_token('hedy@alterra.id')

        data = {
            'name': '',
            'id_outlet': '',
            'type': '',
            'start_time': '01-01-2019',
            'end_time': '01-01-2099',
            'amount_sort': 'asc',
        }

        endpoint = '/report/inventory-log'
        endpoint = endpoint + '?name=' + data['name']
        endpoint = endpoint + '&id_outlet=' + str(data['id_outlet'])
        endpoint = endpoint + '&type=' + data['type']
        endpoint = endpoint + '&start_time=' + data['start_time']
        endpoint = endpoint + '&end_time=' + data['end_time']
        endpoint = endpoint + '&amount_sort=' + data['amount_sort']

        data_1 = {
            'stock': 1000,
            'price': 15000
        }

        data_2 = {
            'stock': 1200,
            'price': 13000
        }

        data_3 = {
            'stock': 800,
            'price': 14000
        }

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
        res = client.put('/inventory/add-stock/1', json = data_1, headers={'Authorization': 'Bearer ' + token})
        res = client.put('/inventory/add-stock/2', json = data_2, headers={'Authorization': 'Bearer ' + token})
        res = client.put('/inventory/add-stock/3', json = data_3, headers={'Authorization': 'Bearer ' + token})
        res = client.post('/product/checkout', json = cart, headers={'Authorization': 'Bearer ' + token})
        res = client.get(endpoint, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # Inventory Log (Case 3: Default)
    def test_inventory_log_report_case_3(self, client):
        # Prepare the DB and token
        db_reset()
        token = create_token('hedy@alterra.id')

        data = {
            'name': '',
            'id_outlet': '',
            'type': 'Keluar',
            'start_time': '',
            'end_time': '',
            'amount_sort': 'desc',
        }

        endpoint = '/report/inventory-log'
        endpoint = endpoint + '?name=' + data['name']
        endpoint = endpoint + '&id_outlet=' + str(data['id_outlet'])
        endpoint = endpoint + '&type=' + data['type']
        endpoint = endpoint + '&start_time=' + data['start_time']
        endpoint = endpoint + '&end_time=' + data['end_time']
        endpoint = endpoint + '&amount_sort=' + data['amount_sort']

        data_1 = {
            'stock': 1000,
            'price': 15000
        }

        data_2 = {
            'stock': 1200,
            'price': 13000
        }

        data_3 = {
            'stock': 800,
            'price': 14000
        }

        cart = {
            'id_outlet': 1,
            'id_customers': 1,
            'item_list': [
                {'id': 1, 'unit': 2, 'price': 12000},
                {'id': 2, 'unit': 1, 'price': 16000},
                {'id': 3, 'unit': 3, 'price': 15000},
                {'id': 4, 'unit': 1, 'price': 12000},
                {'id': 5, 'unit': 1, 'price': 22000}
            ],
            'promo': '',
            'payment_method': 'Tunai',
            'paid_price': 200000,
            'name': 'Lelianto Eko Pradana',
            'phone': '',
            'email': ''
        }

        # Test the endpoints
        res = client.put('/inventory/add-stock/1', json = data_1, headers={'Authorization': 'Bearer ' + token})
        res = client.put('/inventory/add-stock/2', json = data_2, headers={'Authorization': 'Bearer ' + token})
        res = client.put('/inventory/add-stock/3', json = data_3, headers={'Authorization': 'Bearer ' + token})
        res = client.post('/product/checkout', json = cart, headers={'Authorization': 'Bearer ' + token})
        res = client.get(endpoint, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # get report category
    def test_report_category(self, client):
        # Prepare the DB and token
        db_reset()
        token = create_token('hedy@alterra.id')

        # Test the endpoints
        res = client.get("/report/category?start_time=01-02-2020&end_time=02-02-2020", headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    # get report category with correct input 
    def test_report_category_fix_time(self, client):
        # Prepare the DB and token
        db_reset()
        token = create_token('hedy@alterra.id')

        # Test the endpoints
        res = client.get("/report/category?start_time=13-02-2020&end_time=14-02-2020", headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    # get report category fix (sort 1)
    def test_report_category_sort_1(self, client):
        # Prepare the DB and token
        db_reset()
        token = create_token('hedy@alterra.id')

        # Test the endpoints
        res = client.get("/report/category?total_sold_sort=desc&total_sales_sort=asc&start_time=13-02-2020&end_time=14-02-2020", headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    # get report category fix (sort 2)
    def test_report_category_sort_2(self, client):
        # Prepare the DB and token
        db_reset()
        token = create_token('hedy@alterra.id')

        # Test the endpoints
        res = client.get("/report/category?total_sold_sort=asc&total_sales_sort=desc&start_time=13-02-2020&end_time=14-02-2020", headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # get report category fix (sort deleted)
    def test_report_category_sort_deleted(self, client):
        # Prepare the DB and token
        db_reset()
        token = create_token('hedy@alterra.id')

        # Test the endpoints
        res = client.delete("/product/1", headers={'Authorization': 'Bearer ' + token})
        res = client.delete("/product/2", headers={'Authorization': 'Bearer ' + token})
        res = client.delete("/product/3", headers={'Authorization': 'Bearer ' + token})
        res = client.delete("/product/4", headers={'Authorization': 'Bearer ' + token})
        res = client.delete("/product/5", headers={'Authorization': 'Bearer ' + token})
        res = client.get("/report/category?total_sold_sort=asc&total_sales_sort=desc&start_time=13-02-2020&end_time=14-02-2020", headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # get report outlet valid
    def test_report_outlet_valid(self, client):
        # Prepare the DB and token
        db_reset()
        token = create_token('hedy@alterra.id')

        # Test the endpoints
        res = client.get("/report/outlet-sales?start_time=13-02-2020&end_time=14-02-2020&name_outlet=", headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # get report outlet invalid
    def test_report_outlet_invalid(self, client):
        # Prepare the DB and token
        db_reset()
        token = create_token('hedy@alterra.id')

        # Test the endpoints
        res = client.get("/report/outlet-sales?start_time=14-02-2020&end_time=13-02-2020&name_outlet=", headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 400
    
    # get report outlet valid no param
    def test_report_outlet_valid_no_param(self, client):
        # Prepare the DB and token
        db_reset()
        token = create_token('hedy@alterra.id')

        # Test the endpoints
        res = client.get("/report/outlet-sales?start_time=&end_time=&name_outlet=", headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    # get report outlet valid with otlet
    def test_report_outlet_valid_outlet(self, client):
        # Prepare the DB and token
        db_reset()
        token = create_token('hedy@alterra.id')

        # Test the endpoints
        res = client.get("/report/outlet-sales?start_time=13-02-2020&end_time=14-02-2020&name_outlet=Surabaya", headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    # get report outlet valid sort deleted
    def test_report_outlet_valid_sort_deleted(self, client):
        # Prepare the DB and token
        db_reset()
        token = create_token('hedy@alterra.id')

        # Test the endpoints
        res = client.delete("/outlet/1", headers={'Authorization': 'Bearer ' + token})
        res = client.get("/report/outlet-sales?start_time=13-02-2020&end_time=14-02-2020&name_outlet=Surabaya", headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    # get report all outlet valid sort deleted
    def test_report_all_outlet_valid_sort_deleted(self, client):
        # Prepare the DB and token
        db_reset()
        token = create_token('hedy@alterra.id')

        # Test the endpoints
        res = client.delete("/outlet/1", headers={'Authorization': 'Bearer ' + token})
        res = client.get("/report/outlet-sales?start_time=13-02-2020&end_time=14-02-2020", headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # get report profit valid no param
    def test_report_profit_valid_no_param(self, client):
        # Prepare the DB and token
        db_reset()
        token = create_token('hedy@alterra.id')

        # Test the endpoints
        res = client.get("/report/profit?start_time=&end_time=&name_outlet=", headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    # get report profit invalid time
    def test_report_profit_invalid_time(self, client):
        # Prepare the DB and token
        db_reset()
        token = create_token('hedy@alterra.id')

        # Test the endpoints
        res = client.get("/report/profit?start_time=14-02-2020&end_time=13-02-2020&name_outlet=", headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 400
    
    # get report profit valid with outlet
    def test_report_profit_valid_outlet(self, client):
        # Prepare the DB and token
        db_reset()
        token = create_token('hedy@alterra.id')

        # Test the endpoints
        res = client.get("/report/profit?start_time=13-02-2020&end_time=14-02-2020&name_outlet=Surabaya", headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # get report profit valid (sort 1)
    def test_report_profit_sort_1(self, client):
        # Prepare the DB and token
        db_reset()
        token = create_token('hedy@alterra.id')

        # Test the endpoints
        res = client.get("/report/profit?start_time=01-02-2020&end_time=14-02-2021&total_sales_sort=asc&total_inventory_sort=desc&profit_sort=desc", headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    # get report profit valid (sort 2)
    def test_report_profit_sort_2(self, client):
        # Prepare the DB and token
        db_reset()
        token = create_token('hedy@alterra.id')

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

        second_cart = {
            'id_outlet': 2,
            'id_customers': 1,
            'item_list': [
                {'id': 1, 'unit': 1, 'price': 8000}
            ],
            'promo': '',
            'payment_method': 'Tunai',
            'paid_price': 10000,
            'name': 'Lelianto Eko Pradana',
            'phone': '',
            'email': ''
        }
    
        third_cart = {
            'id_outlet': 3,
            'id_customers': 1,
            'item_list': [
                {'id': 1, 'unit': 1, 'price': 5000}
            ],
            'promo': '',
            'payment_method': 'Tunai',
            'paid_price': 10000,
            'name': 'Lelianto Eko Pradana',
            'phone': '',
            'email': ''
        }

        # Test the endpoints
        res = client.post('/product/checkout', json = cart, headers={'Authorization': 'Bearer ' + token})
        res = client.post('/product/checkout', json = second_cart, headers={'Authorization': 'Bearer ' + token})
        res = client.post('/product/checkout', json = third_cart, headers={'Authorization': 'Bearer ' + token})
        res = client.get("/report/profit?start_time=01-02-2020&end_time=14-02-2021&total_sales_sort=desc&total_inventory_sort=asc&profit_sort=asc", headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # testing option
    def test_option(self, client):
        # Test the endpoints
        res = client.options('/report/product-sales')
        res = client.options('/report/category')
        res = client.options('/report/outlet-sales')
        res = client.options('/report/profit')
        res = client.options('/report/history')
        res = client.options('/report/inventory-log')
        assert res.status_code == 200