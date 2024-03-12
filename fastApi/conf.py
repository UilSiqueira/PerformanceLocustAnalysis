from faker import Faker
import random
import requests
from typing import Dict
import json

faker = Faker()

NAME_CATEGORY = "Random Category"
SLUG_CATEGORY = "random-category"


def register(client: requests):
        register_url =  '/user/register'
        username = faker.user_name()
        password = faker.password()

        register_payload = {
            "username": username,
            "password": password
        }

        response = client.post(register_url, json=register_payload, headers={"Content-Type": "application/json"})
        print('User registered - Status Code: ', response.status_code, '\n')
        return {'username': username, 'password': password}


def login(client: requests, credentials: Dict):
        login_url =  '/user/login'

        username = credentials['username']
        password = credentials['password']
        login_payload = {
            "username": username,
            "password": password
        }
        
        response = client.post(login_url, data=login_payload, headers={"Content-Type": "application/x-www-form-urlencoded"})
        token = response.json().get("access_token")

        print('User loged in - Status Code: ', response.status_code, '\n')
        return token


def add_category(client: requests, user_token: Dict, name: str = NAME_CATEGORY, slug: str = SLUG_CATEGORY):
    category_url =  '/category/add'    

    category_payload = {'name': name, 'slug': slug}
    response = client.post(category_url, json=category_payload, 
                                headers={"Content-Type": "application/json",  'Authorization': user_token})

    print(f"Add category - Status Code: {response.status_code} \n")


def add_product(client: requests, user_token: Dict, product_slug: str = None, category_slug: str = SLUG_CATEGORY):
    product_url =  '/product/add'
    faker = Faker()

    fake_slug = faker.word()
    slug = product_slug or fake_slug
    name = slug.capitalize()
    price =  round(random.uniform(10.0, 50.0), 2)
    stock = random.randint(5, 35)

    product_payload = {
        'category_slug': category_slug,
        'product': {
            'name': name,
            'slug': slug,
            'price': price,
            'stock': stock
        }
    }
    response = client.post(product_url, json=product_payload, 
                           headers={"Content-Type": "application/json", 'Authorization': user_token})
    
    print(f"Add product - Status Code: {response.status_code}\n")


def set_product_list(client: requests, user_token: Dict, product_slug: str = None, category_slug: str = SLUG_CATEGORY):
    list_url =  f'/product/list?search={product_slug}'

    response = client.get(list_url, headers={"Content-Type": "application/json",  'Authorization': user_token})
    result = json.loads(response.text)
    if not result.get('items', None):
        add_product(client, user_token, product_slug, category_slug)
        print("Set product added\n")
        return

    print(f"Set products - Status Code: {response.status_code} - Product already exists\n")


def set_category(client: requests, user_token: Dict, name: str = NAME_CATEGORY, slug: str = SLUG_CATEGORY):
    list_url =  '/category/list'
    response = client.get(list_url, headers={"Content-Type": "application/json",  'Authorization': user_token})
    result = json.loads(response.text)
    if result:
        for category in result:
            if category.get('name', None) == name:
                print(f"Set category - Status Code: {response.status_code} - Category already exists\n")
                return

    add_category(client, user_token, name, slug)

      