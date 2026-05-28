import unittest
import json
import base64
from app import create_app, db
from app.models import Role, Category, User

class APICategoriesTestCase(unittest.TestCase):
    def setUp(self):
        # Configure application for isolated testing environment
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        
        # Create a confirmed test user to pass global API authentication checks
        self.user = User(email='test@example.com', username='testuser', password='password', confirmed=True)
        db.session.add(self.user)
        db.session.commit()
        
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_api_headers(self):
        """Generates standard API headers alongside HTTP Basic Authentication credentials"""
        auth_string = f'test@example.com:password'
        auth_b64 = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')
        return {
            'Authorization': f'Basic {auth_b64}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_1_create_category_positive(self):
        """Positive Test: Successfully create a new category via POST"""
        response = self.client.post(
            '/api/v1/categories/',
            headers=self.get_api_headers(),
            data=json.dumps({'name': 'Technology'})
        )
        self.assertEqual(response.status_code, 201)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['name'], 'Technology')
        self.assertEqual(json_response['posts_count'], 0)
        self.assertIsNotNone(json_response['id'])

    def test_2_create_category_negative_missing_name(self):
        """Negative Test: Try to create a category with an empty payload"""
        response = self.client.post(
            '/api/v1/categories/',
            headers=self.get_api_headers(),
            data=json.dumps({})
        )
        self.assertEqual(response.status_code, 400)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['error'], 'bad request')
        self.assertEqual(json_response['message'], 'Category name is missing.')

    def test_3_create_category_negative_duplicate(self):
        """Negative Test: Try to create a category name that already exists"""
        c = Category(name='Programming')
        db.session.add(c)
        db.session.commit()

        response = self.client.post(
            '/api/v1/categories/',
            headers=self.get_api_headers(),
            data=json.dumps({'name': 'Programming'})
        )
        self.assertEqual(response.status_code, 400)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['message'], 'Category name already exists.')

    def test_4_get_all_categories(self):
        """Positive Test: Read all categories via GET"""
        c1 = Category(name='Education')
        c2 = Category(name='Health')
        db.session.add_all([c1, c2])
        db.session.commit()

        response = self.client.get('/api/v1/categories/', headers=self.get_api_headers())
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertIn('categories', json_response)
        self.assertEqual(len(json_response['categories']), 2)

    def test_5_get_single_category_positive(self):
        """Positive Test: Read a single category by ID via GET"""
        c = Category(name='Science')
        db.session.add(c)
        db.session.commit()

        response = self.client.get(f'/api/v1/categories/{c.id}', headers=self.get_api_headers())
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['name'], 'Science')

    def test_6_get_single_category_negative_not_found(self):
        """Negative Test: Request a non-existent category ID"""
        response = self.client.get('/api/v1/categories/999', headers=self.get_api_headers())
        self.assertEqual(response.status_code, 404)

    def test_7_update_category_positive(self):
        """Positive Test: Update a category name via PUT"""
        c = Category(name='Lifestyle')
        db.session.add(c)
        db.session.commit()

        response = self.client.put(
            f'/api/v1/categories/{c.id}',
            headers=self.get_api_headers(),
            data=json.dumps({'name': 'Life & Style'})
        )
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['name'], 'Life & Style')

    def test_8_update_category_negative_missing_name(self):
        """Negative Test: Try updating a category with an empty payload"""
        c = Category(name='Sports')
        db.session.add(c)
        db.session.commit()

        response = self.client.put(
            f'/api/v1/categories/{c.id}',
            headers=self.get_api_headers(),
            data=json.dumps({})
        )
        self.assertEqual(response.status_code, 400)

    def test_9_delete_category_positive(self):
        """Positive Test: Delete an existing category via DELETE"""
        c = Category(name='Gaming')
        db.session.add(c)
        db.session.commit()

        response = self.client.delete(f'/api/v1/categories/{c.id}', headers=self.get_api_headers())
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(Category.query.get(c.id))