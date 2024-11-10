import unittest
import json
from flask import Flask
from main import app  # Import your Flask app

class ReceiptAPITestCase(unittest.TestCase):
    def setUp(self):
        # Set up the test client
        self.app = app.test_client()
        self.app.testing = True

    def test_process_receipt_points(self):
        # Simulate sending a valid POST request to /receipts/process
        receipt_data = {
            "retailer": "Target",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [
                {
                "shortDescription": "Mountain Dew 12PK",
                "price": "6.49"
                },{
                "shortDescription": "Emils Cheese Pizza",
                "price": "12.25"
                },{
                "shortDescription": "Knorr Creamy Chicken",
                "price": "1.26"
                },{
                "shortDescription": "Doritos Nacho Cheese",
                "price": "3.35"
                },{
                "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
                "price": "12.00"
                }
            ],
            "total": "35.35"
        }
        
        response = self.app.post('/receipts/process', 
                                 data=json.dumps(receipt_data), 
                                 content_type='application/json')
        response_data = response.data.decode('utf-8')
        data = json.loads(response_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', data)
    
    def test_process_receipt_points_no_data(self):
        # Simulate sending a POST request with no data to /receipts/process
        response = self.app.post('/receipts/process', data=json.dumps({}), content_type='application/json')
        response_data = response.data.decode('utf-8')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response_data)
        self.assertEqual(data['error'], 'No receipt data provided')

    def test_get_receipt_points(self):
        # Simulate first creating a receipt, then fetching its points
        receipt_data = {
            "retailer": "Target",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [
                {
                "shortDescription": "Mountain Dew 12PK",
                "price": "6.49"
                },{
                "shortDescription": "Emils Cheese Pizza",
                "price": "12.25"
                },{
                "shortDescription": "Knorr Creamy Chicken",
                "price": "1.26"
                },{
                "shortDescription": "Doritos Nacho Cheese",
                "price": "3.35"
                },{
                "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
                "price": "12.00"
                }
            ],
            "total": "35.35"
        }
        
        process_response = self.app.post('/receipts/process',
                                         data=json.dumps(receipt_data),
                                         content_type='application/json')
        self.assertEqual(process_response.status_code, 200)
        process_response_data = process_response.data.decode('utf-8')
        process_data = json.loads(process_response_data)
        receipt_id = process_data['id']

        # Simulate sending a GET request to /receipts/<receipt_id>/points
        points_response = self.app.get(f'/receipts/{receipt_id}/points')
        self.assertEqual(points_response.status_code, 200)
        points_response_data = points_response.data.decode('utf-8')
        points_data = json.loads(points_response_data)
        self.assertEqual(points_data['id'], receipt_id)
        self.assertIn('points', points_data)
        self.assertEqual(points_data['points'], 28)

    def test_get_receipt_points_not_found(self):
        # Simulate sending a GET request for a non-existent receipt
        response = self.app.get('/receipts/non_existent_receipt_id/points')
        self.assertEqual(response.status_code, 404)
        response_data = response.data.decode('utf-8')
        data = json.loads(response_data)
        self.assertEqual(data['error'], 'Receipt not found')

if __name__ == '__main__':
    unittest.main()
