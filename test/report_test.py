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
