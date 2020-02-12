import json
from . import app, client, create_token, db_reset, cache

class TestReport():
    # Product Report (Case 1 - All filter without date)
    def test_product_report_case_1(self, client):
        # Prepare the DB and token
        db_reset()
        token = create_token('hedy@alterra.id')

        data = {
            'name': '',
            'category': '',
            'id_outlet': '',
            'start_time': '',
            'end_time': '',
        }

        # Test the endpoints
        res = client.post('/inventory/1', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 400
