import json
from . import app, client, create_token, db_reset, cache

class TestProducts():
    # Get all product from specified owner (accessed by owner)
    def test_get_all_products_owner(self, client):
        # Prepare the DB and token
        db_reset()
        token = create_token('hedy@alterra.id')

        # Test the endpoints
        res = client.get('/product', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    # Get all product from specified owner (accessed by admin)
    def test_get_all_products_admin(self, client):
        # Prepare the DB and token
        db_reset()
        token = create_token('stevejobs')

        # Test the endpoints
        res = client.get('/product', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    # Get all product from specified owner (accessed by cashier with filter)
    def test_get_all_products_cashier_1(self, client):
        # Prepare the DB and token
        db_reset()
        token = create_token('budisetiawan')

        data = {
            'category': 'Mie Ayam',
            'show': 'Ya',
            'name': 'Mi' 
        }

        # Test the endpoints
        res = client.get('/product', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    # Get all product from specified owner (accessed by cashier with filter)
    def test_get_all_products_cashier_2(self, client):
        # Prepare the DB and token
        db_reset()
        token = create_token('budisetiawan')

        data = {
            'category': 'Mie Ayam',
            'show': 'Tidak',
            'name': 'Mi' 
        }

        # Test the endpoints
        res = client.get('/product', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # Success add new product (new ingredients)
    def test_add_product_new_ingredients(self, client):
        # Prepare the DB and token
        db_reset()
        token = create_token('stevejobs')

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
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # Success add new product (ingredients exist)
    def test_add_product_exist_ingredients(self, client):
        # Prepare the DB and token
        token = create_token('hedy@alterra.id')

        data = {
            "name": "Indomie Malang",
            "category": "Indomie",
            "price": 10000,
            "show": "Tidak",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT5gLpyIuURwUvD41khAPpAvJ1dteWvXM1S_pePXKbQ9YjRhLrA6Q&s",
            "recipe": [
                {"name": "Indomie Jakarta", "quantity": 1, "unit": "pcs"},
                {"name": "Cabe Merah", "quantity": 30, "unit": "gram"},
                {"name": "Cabe Hijau", "quantity": 30, "unit": "gram"}]
        }

        # Test the endpoints
        res = client.post('/product', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # Success add new product (without recipe)
    def test_add_product_without_recipe(self, client):
        # Prepare the DB and token
        token = create_token('stevejobs')

        data = {
            "name": "Mie Ayam Bakso",
            "category": "Mie Ayam",
            "price": 10000,
            "show": "Ya",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT5gLpyIuURwUvD41khAPpAvJ1dteWvXM1S_pePXKbQ9YjRhLrA6Q&s",
            "recipe": []
        }

        # Test the endpoints
        res = client.post('/product', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # Add new product failed (empty field)
    def test_add_product_empty_field(self, client):
        # Prepare the DB and token
        token = create_token('stevejobs')

        data = {
            "name": "",
            "category": "",
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
        res_json = json.loads(res.data)
        assert res.status_code == 400
        assert res_json['message'] == 'Tidak boleh ada kolom yang dikosongkan'

    # Add new product failed (dulplicate entry)
    def test_add_product_duplicate_entry(self, client):
        # Prepare the DB and token
        token = create_token('stevejobs')

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
        res_json = json.loads(res.data)
        assert res.status_code == 409

    # Get product by ID (not found)
    def test_get_product_by_id_not_found(self, client):
        # Prepare the DB and token
        token = create_token('stevejobs')

        # Test the endpoints
        res = client.get('/product/2020', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    # Get product by ID (success)
    def test_get_product_by_id_success_1(self, client):
        # Prepare the DB and token
        token = create_token('stevejobs')

        # Test the endpoints
        res = client.get('/product/5', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    # Get product by ID (success)
    def test_get_product_by_id_success_2(self, client):
        # Prepare the DB and token
        token = create_token('stevejobs')

        # Test the endpoints
        res = client.get('/product/6', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    # Edit product failed (empty field)
    def test_edit_product_empty_field(self, client):
        # Prepare the DB and token
        token = create_token('hedy@alterra.id')

        data = {
            "name": "",
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
        res = client.put('/product/5', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 400
    
    # Edit product success (Case 1 : Add new ingredients)
    def test_edit_product_success_case_1(self, client):
        # Prepare the DB and token
        token = create_token('stevejobs')

        data = {
            "name": "Indomie Bandung",
            "category": "Mie",
            "price": 10000,
            "show": "Tidak",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT5gLpyIuURwUvD41khAPpAvJ1dteWvXM1S_pePXKbQ9YjRhLrA6Q&s",
            "recipe": [
                {"name": "Indomie Jakarta", "quantity": 1, "unit": "pcs"},
                {"name": "Cabe Merah", "quantity": 30, "unit": "gram"},
                {"name": "Cabe Hijau", "quantity": 30, "unit": "gram"},
                {"name": "Bawang Goreng", "quantity": 30, "unit": "gram"}]
        }

        # Test the endpoints
        res = client.put('/product/5', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # Edit product success (Case 2 : Remove some ingredients)
    def test_edit_product_success_case_1(self, client):
        # Prepare the DB and token
        token = create_token('stevejobs')

        data = {
            "name": "Indomie Bandung",
            "category": "Indomie",
            "price": 12000,
            "show": "Ya",
            "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT5gLpyIuURwUvD41khAPpAvJ1dteWvXM1S_pePXKbQ9YjRhLrA6Q&s",
            "recipe": [
                {"name": "Indomie Bandung", "quantity": 1, "unit": "pcs"},
                {"name": "Cabe Merah", "quantity": 30, "unit": "gram"},
                {"name": "Bawang Goreng", "quantity": 30, "unit": "gram"}]
        }

        # Test the endpoints
        res = client.put('/product/5', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    # Soft delete product success
    def test_soft_delete_product(self, client):
        # Prepare the DB and token
        token = create_token('stevejobs')

        # Test the endpoints
        res = client.delete('/product/6', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    # Get all category
    def test_get_all_category(self, client):
        # Prepare the DB and token
        token = create_token('stevejobs')

        # Test the endpoints
        res = client.get('/product/category', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    # Get all category_owner_access
    def test_get_all_category_owner_access(self, client):
        # Prepare the DB and token
        token = create_token('hedy@alterra.id')

        # Test the endpoints
        res = client.get('/product/category', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # Get all product per category (Case 1 : Product exist)
    def test_get_product_by_category_case_1(self, client):
        # Prepare the DB and token
        token = create_token('hedy@alterra.id')

        # Test the endpoints
        res = client.get('/product/category/items?category=Indomie', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # Get all product per category (Case 2 : Product doesn't exist)
    def test_get_product_by_category_case_2(self, client):
        # Prepare the DB and token
        token = create_token('stevejobs')

        # Test the endpoints
        res = client.get('/product/category/items?category=Ayam', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # Checkout (Case 1 : No active transaction)
    def test_checkout_case_1(self, client):
        # Prepare the DB and token
        token = create_token('budisetiawan')

        # Test the endpoints
        res = client.get('/product/checkout/2703', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 404

    # Checkout (Case 2 : Cashier is employee)
    def test_checkout_case_2(self, client):
        # Prepare the DB and token
        token = create_token('budisetiawan')

        # Test the endpoints
        res = client.get('/product/checkout/1', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200
    
    # Checkout (Case 3 : Cashier is owner)
    def test_checkout_case_3(self, client):
        # Prepare the DB and token
        token = create_token('hedy@alterra.id')

        # Test the endpoints
        res = client.get('/product/checkout/2', headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200

    # Send order (Case 1 : empty field)
    def test_send_order_case_1(self, client):
        # Prepare the DB and token
        token = create_token('hedy@alterra.id')

        data = {
            "id_outlet": "",
            "id_customers": "",
            "item_list": [
                {"id": 1, "unit": 2, "price": 24000},
                {"id": 2, "unit": 1, "price": 15000}],
            "promo": "",
            "payment_method": "Tunai",
            "paid_price": 50000,
            "name": "Bob",
            "phone": "",
            "email": ""
        }

        # Test the endpoints
        res = client.post('/product/checkout', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 400

    # Send order (Case 2 : wrong input)
    def test_send_order_case_2(self, client):
        # Prepare the DB and token
        token = create_token('hedy@alterra.id')

        data = {
            "id_outlet": 1,
            "id_customers": "",
            "item_list": [
                {"id": 1, "unit": 2, "price": 12000},
                {"id": 2, "unit": 1, "price": 15000}],
            "promo": "",
            "payment_method": "Tunai",
            "paid_price": 30000,
            "name": "Bob",
            "phone": "",
            "email": ""
        }

        # Test the endpoints
        res = client.post('/product/checkout', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 422

    # Send order (Case 3 : success, cashier is employee and customer is member)
    def test_send_order_case_3(self, client):
        # Prepare the DB and token
        token = create_token('budisetiawan')

        data = {
            "id_outlet": 1,
            "id_employee": 1,
            "id_customers": 1,
            "item_list": [
                {"id": 1, "unit": 2, "price": 12000},
                {"id": 5, "unit": 1, "price": 9000}],
            "promo": "",
            "payment_method": "Tunai",
            "paid_price": 50000,
            "name": "Buzz Lightyear",
            "phone": "",
            "email": ""
        }

        # Test the endpoints
        res = client.post('/product/checkout', json = data, headers={'Authorization': 'Bearer ' + token})
        res_json = json.loads(res.data)
        assert res.status_code == 200