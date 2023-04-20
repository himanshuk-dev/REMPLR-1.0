from unittest import TestCase
from flask import session, request, redirect
from app import app, db, Nutritionist, Client, RegisterForm

class RootTestCase(TestCase):
    
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql///remplr_test'
        db.create_all()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        
    def test_root_with_nutritionist(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['nutritionist_id'] = 1
                
            nutritionist = Nutritionist(id=1, name='John Doe')
            db.session.add(nutritionist)
            db.session.commit()
            
            response = c.get('/')
            
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'John Doe', response.data)
            
    def test_root_with_client(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess['client_id'] = 1
                
            client = Client(id=1, name='Jane Doe')
            db.session.add(client)
            db.session.commit()
            
            response = c.get('/')
            
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Jane Doe', response.data)
            
    def test_root_without_user(self):
        response = self.client.get('/')
        
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'John Doe', response.data)
        self.assertNotIn(b'Jane Doe', response.data)
        
    def test_register_page(self):
        response = self.client.get('/Register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration', response.data)
        
    def test_register_nutritionist_success(self):
        data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'confirm_password': 'testpassword'
        }
        
        response = self.client.post('/register/nutritionist', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Successfully Created Your Account!', response.data)
        
        with self.client as c:
            with c.session_transaction() as sess:
                self.assertTrue(sess['nutritionist_id'])
                
    def test_register_nutritionist_existing_user(self):
        nutritionist = Nutritionist(username='testuser', email='testuser@example.com', first_name='Test', last_name='User')
        db.session.add(nutritionist)
        db.session.commit()
        
        data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'confirm_password': 'testpassword'
        }
        
        response = self.client.post('/register/nutritionist', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'The username or email is already taken', response.data)
        
    def test_register_nutritionist_invalid_form(self):
        data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'invalid_email',
            'password': 'testpassword',
            'confirm_password': 'testpassword'
        }
        
        response = self.client.post('/register/nutritionist', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid email address.', response.data)        
    