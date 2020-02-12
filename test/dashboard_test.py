import json
from . import app, client, create_token, db_reset, cache

class TestDashboard():
    # testing display dashboard valid (outlet)
    def test_display_outlet_valid_outlet(self, client):
        # get token 
        token = create_token('hedy@alterra.id')
        # Prepare the DB
        db_reset()

        # Test the endpoints
        res = client.get('/dashboard?name_outlet=Surabaya', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    # testing display dashboard valid (interval hari ini)
    def test_display_outlet_valid_inteval_hari_ini(self, client):
        # get token 
        token = create_token('hedy@alterra.id')
        # Prepare the DB
        db_reset()

        # Test the endpoints
        res = client.get('/dashboard?date_interval=Hari ini', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    # testing display dashboard valid (interval Kemarin)
    def test_display_outlet_valid_inteval_kemarin(self, client):
        # get token 
        token = create_token('hedy@alterra.id')
        # Prepare the DB
        db_reset()

        # Test the endpoints
        res = client.get('/dashboard?date_interval=Kemarin', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # testing display dashboard valid (interval minggu ini)
    def test_display_outlet_valid_inteval_minggu_ini(self, client):
        # get token 
        token = create_token('hedy@alterra.id')
        # Prepare the DB
        db_reset()

        # Test the endpoints
        res = client.get('/dashboard?date_interval=Minggu ini', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    # testing display dashboard valid (interval bulan ini)
    def test_display_outlet_valid_inteval_bulan_ini(self, client):
        # get token 
        token = create_token('hedy@alterra.id')
        # Prepare the DB
        db_reset()

        # Test the endpoints
        res = client.get('/dashboard?date_interval=Bulan ini', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
        
    # testing display dashboard valid (interval bulan lalu)
    def test_display_outlet_valid_inteval_bulan_lalu(self, client):
        # get token 
        token = create_token('hedy@alterra.id')
        # Prepare the DB
        db_reset()

        # Test the endpoints
        res = client.get('/dashboard?date_interval=Bulan lalu', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    # testing display dashboard valid (start_time. end_time)
    def test_display_outlet_valid_inteval_start_end_time(self, client):
        # get token 
        token = create_token('hedy@alterra.id')
        # Prepare the DB
        db_reset()

        # Test the endpoints
        res = client.get('/dashboard?start_time=04-02-2020&end_time=05-02-2020', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # testing display dashboard valid (month)
    def test_display_outlet_valid_month(self, client):
        # get token 
        token = create_token('hedy@alterra.id')
        # Prepare the DB
        db_reset()

        # Test the endpoints
        res = client.get('/dashboard?month=1', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    
    # testing display dashboard valid (5 product)
    def test_display_outlet_valid_five_product(self, client):
        # get token 
        token = create_token('hedy@alterra.id')
        # Prepare the DB
        db_reset()
        
        #create one product
        data = {
            "name": "Indomie Jakarta",
            "category": "Indomie",
            "price": 9000,
            "show": "Ya",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT5gLpyIuURwUvD41khAPpAvJ1dteWvXM1S_pePXKbQ9YjRhLrA6Q&s",
            "recipe": [
                {"name": "Indomie Jakarta", "quantity": 1, "unit": "pcs"},
                {"name": "Cabe Merah", "quantity": 30, "unit": "gram"},
                {"name": "Cabe Hijau", "quantity": 30, "unit": "gram"}]
        }

        # Test the endpoints
        res = client.post('/product', json = data, headers={'Authorization': 'Bearer ' + token})
        res = client.get('/dashboard', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    # testing display dashboard valid (5 product with outlet)
    def test_display_outlet_valid_five_product_outlet(self, client):
        # get token 
        token = create_token('hedy@alterra.id')
        # Prepare the DB
        db_reset()
        
        #create one product
        data = {
            "name": "Indomie Jakarta",
            "category": "Indomie",
            "price": 9000,
            "show": "Ya",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT5gLpyIuURwUvD41khAPpAvJ1dteWvXM1S_pePXKbQ9YjRhLrA6Q&s",
            "recipe": [
                {"name": "Indomie Jakarta", "quantity": 1, "unit": "pcs"},
                {"name": "Cabe Merah", "quantity": 30, "unit": "gram"},
                {"name": "Cabe Hijau", "quantity": 30, "unit": "gram"}]
        }

        # Test the endpoints
        res = client.post('/product', json = data, headers={'Authorization': 'Bearer ' + token})
        res = client.get('/dashboard?name_outlet=Surabaya', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # testing display dashboard valid (5 catagory)
    def test_display_outlet_valid_five_catagory(self, client):
        # get token 
        token = create_token('hedy@alterra.id')
        # Prepare the DB
        db_reset()
        
        #create one product
        data = {
            "name": "Indomie Jakarta",
            "category": "Indom",
            "price": 9000,
            "show": "Ya",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT5gLpyIuURwUvD41khAPpAvJ1dteWvXM1S_pePXKbQ9YjRhLrA6Q&s",
            "recipe": [
                {"name": "Indomie Jakarta", "quantity": 1, "unit": "pcs"},
                {"name": "Cabe Merah", "quantity": 30, "unit": "gram"},
                {"name": "Cabe Hijau", "quantity": 30, "unit": "gram"}]
        }
        res = client.post('/product', json = data, headers={'Authorization': 'Bearer ' + token})

        data = {
            "name": "Indomie Jakarta",
            "category": "In",
            "price": 9000,
            "show": "Ya",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT5gLpyIuURwUvD41khAPpAvJ1dteWvXM1S_pePXKbQ9YjRhLrA6Q&s",
            "recipe": [
                {"name": "Indomie Jakarta", "quantity": 1, "unit": "pcs"},
                {"name": "Cabe Merah", "quantity": 30, "unit": "gram"},
                {"name": "Cabe Hijau", "quantity": 30, "unit": "gram"}]
        }
        res = client.post('/product', json = data, headers={'Authorization': 'Bearer ' + token})
        
        data = {
            "name": "Indomie Jakarta",
            "category": "Ind",
            "price": 9000,
            "show": "Ya",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT5gLpyIuURwUvD41khAPpAvJ1dteWvXM1S_pePXKbQ9YjRhLrA6Q&s",
            "recipe": [
                {"name": "Indomie Jakarta", "quantity": 1, "unit": "pcs"},
                {"name": "Cabe Merah", "quantity": 30, "unit": "gram"},
                {"name": "Cabe Hijau", "quantity": 30, "unit": "gram"}]
        }
        res = client.post('/product', json = data, headers={'Authorization': 'Bearer ' + token})

        data = {
            "name": "Indomie Jakarta",
            "category": "I",
            "price": 9000,
            "show": "Ya",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT5gLpyIuURwUvD41khAPpAvJ1dteWvXM1S_pePXKbQ9YjRhLrA6Q&s",
            "recipe": [
                {"name": "Indomie Jakarta", "quantity": 1, "unit": "pcs"},
                {"name": "Cabe Merah", "quantity": 30, "unit": "gram"},
                {"name": "Cabe Hijau", "quantity": 30, "unit": "gram"}]
        }
        res = client.post('/product', json = data, headers={'Authorization': 'Bearer ' + token})
        # Test the endpoints
        res = client.get('/dashboard', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # testing display dashboard valid (5 catagory with outlet)
    def test_display_outlet_valid_five_catagory_outlet(self, client):
        # get token 
        token = create_token('hedy@alterra.id')
        # Prepare the DB
        db_reset()
        
        #create one product
        data = {
            "name": "Indomie Jakarta",
            "category": "Indom",
            "price": 9000,
            "show": "Ya",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT5gLpyIuURwUvD41khAPpAvJ1dteWvXM1S_pePXKbQ9YjRhLrA6Q&s",
            "recipe": [
                {"name": "Indomie Jakarta", "quantity": 1, "unit": "pcs"},
                {"name": "Cabe Merah", "quantity": 30, "unit": "gram"},
                {"name": "Cabe Hijau", "quantity": 30, "unit": "gram"}]
        }
        res = client.post('/product', json = data, headers={'Authorization': 'Bearer ' + token})

        data = {
            "name": "Indomie Jakarta",
            "category": "In",
            "price": 9000,
            "show": "Ya",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT5gLpyIuURwUvD41khAPpAvJ1dteWvXM1S_pePXKbQ9YjRhLrA6Q&s",
            "recipe": [
                {"name": "Indomie Jakarta", "quantity": 1, "unit": "pcs"},
                {"name": "Cabe Merah", "quantity": 30, "unit": "gram"},
                {"name": "Cabe Hijau", "quantity": 30, "unit": "gram"}]
        }
        res = client.post('/product', json = data, headers={'Authorization': 'Bearer ' + token})
        
        data = {
            "name": "Indomie Jakarta",
            "category": "Ind",
            "price": 9000,
            "show": "Ya",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT5gLpyIuURwUvD41khAPpAvJ1dteWvXM1S_pePXKbQ9YjRhLrA6Q&s",
            "recipe": [
                {"name": "Indomie Jakarta", "quantity": 1, "unit": "pcs"},
                {"name": "Cabe Merah", "quantity": 30, "unit": "gram"},
                {"name": "Cabe Hijau", "quantity": 30, "unit": "gram"}]
        }
        res = client.post('/product', json = data, headers={'Authorization': 'Bearer ' + token})

        data = {
            "name": "Indomie Jakarta",
            "category": "I",
            "price": 9000,
            "show": "Ya",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT5gLpyIuURwUvD41khAPpAvJ1dteWvXM1S_pePXKbQ9YjRhLrA6Q&s",
            "recipe": [
                {"name": "Indomie Jakarta", "quantity": 1, "unit": "pcs"},
                {"name": "Cabe Merah", "quantity": 30, "unit": "gram"},
                {"name": "Cabe Hijau", "quantity": 30, "unit": "gram"}]
        }
        res = client.post('/product', json = data, headers={'Authorization': 'Bearer ' + token})
        # Test the endpoints
        res = client.get('/dashboard?name_outlet=Surabaya', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200