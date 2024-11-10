from flask import Flask, request, jsonify
from receipthandler import ReceiptHandler
import json

app = Flask(__name__)

rh = ReceiptHandler()

@app.route('/receipts/process', methods=['POST'])
def process_receipt_points():
    receipt_data = request.json  
    if not receipt_data: 
        return jsonify({"error": "No receipt data provided"}), 400

    receipt_id = rh.process_receipt(receipt_data)
    return jsonify({"id": receipt_id}), 200

@app.route('/receipts/<receipt_id>/points', methods=['GET'])
def get_receipt_points(receipt_id):
    points = rh.get_points(receipt_id)
    if points is None:
        return jsonify({"error": "Receipt not found"}), 404

    return jsonify({"id": receipt_id, "points": points}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)