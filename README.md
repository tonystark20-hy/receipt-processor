# receipt-processor

## Overview

The Receipt Processor is a web service that processes receipt data and calculates points based on specific rules. The service provides two main endpoints:

/receipts/process: Accepts receipt data and returns an ID for the processed receipt.
/receipts/{id}/points: Returns the number of points awarded for a receipt given its ID.
This service is built with Go and is containerized using Docker for easy deployment and testing.

## Requirements
* Docker
* Python 3.11

## Getting Started
```
docker build -t receipts-processor .
```
```
docker run -p 8080:8080 receipt-processor
```

## Process Receipts Endpoint

* Path: /receipts/process
* Method: POST
* Payload: Receipt JSON
* Response: JSON containing an id for the receipt.

## Example Receipt JSON:
```
{
    "retailer": "M&M Corner Market",
    "purchaseDate": "2022-03-20",
    "purchaseTime": "14:33",
    "items": [
        {
        "shortDescription": "Gatorade",
        "price": "2.25"
        },{
        "shortDescription": "Gatorade",
        "price": "2.25"
        },{
        "shortDescription": "Gatorade",
        "price": "2.25"
        },{
        "shortDescription": "Gatorade",
        "price": "2.25"
        }
    ],
    "total": "9.00"
}
```

## Example Response:
```
{"id":"7211067a-fd67-4524-91d0-9ecd580f2b7f"}
```

* 400 error if Receipt JSON = {}
* 400 error if purchase date format not in yyyy-mm-dd
* 400 error if purchase time format not int hh:mm

## Get Receipts Endpoint

* Path: /receipts/{id}/points
* Method: GET
* Response: A JSON object containing the number of points awarded.

## Example Response:
```
{"points":28}
```

* 404 error if no matching id

## Testing

DockerFile will automatically test tests/test.py 
to run manually:
```
python -m unittest discover -s tests
```