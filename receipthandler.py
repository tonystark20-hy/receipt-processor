from flask import Flask, request, jsonify
import math
from datetime import datetime
import uuid

class ReceiptHandler:
    def __init__(self):
        self.receipts = {}
        pass

    def process_receipt(self, receipt_data):

        receipt_id = str(uuid.uuid4())  
        points = self.calculate_points(receipt_data)
        self.receipts[receipt_id] = points  
        return receipt_id
        pass

    def get_points(self, receipt_id):
        return self.receipts.get(receipt_id)
        pass

    def calculate_points(self, receipt_data):
        points = 0

        # Rule 1: 1 point for every alphanumeric character in the retailer name
        retailer = receipt_data.get("retailer", "")
        points += sum(1 for c in retailer if c.isalnum())

        # Rule 2: 50 points if the total is a round dollar amount with no cents
        total = float(receipt_data.get("total", 0))
        if total.is_integer():
            points += 50

        # Rule 3: 25 points if the total is a multiple of 0.25
        if total % 0.25 == 0:
            points += 25

        # Rule 4: 5 points for every two items on the receipt
        items = receipt_data.get("items", [])
        points += (len(items) // 2) * 5

        # Rule 5: If the trimmed item description length is a multiple of 3, multiply the price by 0.2 and round up
        for item in items:
            description = item.get("shortDescription", "").strip()
            if len(description) % 3 == 0:
                item_price = float(item.get("price", 0))
                points += round(item_price * 0.2)

        # Rule 6: 6 points if the day in the purchase date is odd
        purchase_date = receipt_data.get("purchaseDate", "")
        try:
            date_obj = datetime.strptime(purchase_date, "%Y-%m-%d")
            if date_obj.day % 2 != 0:
                points += 6
        except ValueError:
            pass  

        # Rule 7: 10 points if the purchase was made after 2:00 PM and before 4:00 PM
        purchase_time = receipt_data.get("purchaseTime", "")
        try:
            time_obj = datetime.strptime(purchase_time, "%H:%M")
            if time_obj.hour == 14 or time_obj.hour == 15 or (time_obj.hour == 16 and time_obj.minute == 0):
                points += 10
        except ValueError:
            pass  

        return points