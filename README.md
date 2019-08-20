# rest_api_with_mongo_db

How to Run:
- Install python 3.6 and create virtualenv
- Install all dependency from requirements.txt file using pip3 install -r requirements.txt in that virtualenv
- I have used a cloud instance of mongodb
- credentials are stored in credentials.json file which is stored separately
- put 'credentials.json' in heady_assignment dir first and runproject with below command:
    1. **python manage.py runserver 0.0.0.0:80**
    It will start the server to accept api request
     
#### List of APIs:

1. API to add category:
    - url: http://localhost/rest_api/category
    - payload: {
        "name": "sample_category",
        "parent": null
    }
    OR
    - payload: {
        "name": "child_category",
        "parent": "sample_category"
    }
    - send a POST request on thi url with this payload (as example)
2. API to add product mapped to a category or categories
    - url: http://localhost/rest_api/product
    - payload: {
        "name": "sample_product",
        "price": 15,
        "currency": "USD",
        "category_list": ["sample_category"]
    }
    - send a POST request on this url with this payload (as example)
    where category is provided in category_list field of payload
3. API to get all the categories with child category
    - url: http://localhost/rest_api/category
    - send a GET request on this url
4. API to get all products by category
    - url: http://localhost/rest_api/product
    - payload: {"category": "sample_category"}
    - send a GET request with this payload
5. API to update product details
    - url: http://localhost/rest_api/product
    - payload: {
        "name": "sample_product",
        "price": <new price>,
        "currency": <new currency>,
        "new_name" <new name of the product>        
    }
    - Send an PUT request with this payload
    