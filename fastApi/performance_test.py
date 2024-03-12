from locust import HttpUser, task, between
from redirect_handle import redirect_handle
from conf import login, register, add_product, set_category, set_product_list
from collections import deque
import json
from faker import Faker
faker = Faker()


class WebsiteUser(HttpUser):
    wait_time = between(3, 10)
    
    def on_start(self):
        self.credentials = register(self.client)
        self.user = login(self.client, self.credentials)
        self.user_token = f"Bearer {self.user}"
        self.slug_for_search = 'product-slug'
        set_category(self.client, self.user_token)
        set_product_list(self.client, self.user_token, self.slug_for_search)

    @redirect_handle
    @task(3)
    def list_products_page(self):
        page: int = 1
        size: int = 50
        # list_url =  '/product/list'
        # list_url =  f'/product/list/{search}'
        list_url = f'/product/list?page={page}&size={size}'
  
        response = self.client.get(list_url, headers={"Content-Type": "application/json",  'Authorization': self.user_token})
        print(f"List all products offset - Status Code: {response.status_code}")
        print(f"All products listed: {len(json.loads(response.text)['items'])}\n")
    
    @redirect_handle
    @task(2)
    def list_product_search(self):
        list_url =  f'/product/list?search={self.slug_for_search}'
  
        response = self.client.get(list_url, headers={"Content-Type": "application/json",  'Authorization': self.user_token})
        print(f"Search products - Status Code: {response.status_code}")
        print(f"Products search listed: {len(json.loads(response.text)['items'])}\n")

    @redirect_handle
    @task(2)
    def post_product_task(self):
        add_product(self.client, self.user_token)

    @redirect_handle
    @task(1)
    def register_task(self):
        register(self.client)

    @redirect_handle
    @task(2)
    def login_task(self):
        login(self.client, self.credentials)
