import requests
import json

class KaceApi:
    def __init__(self, kace_api_username="", kace_api_password="", kace_url="https://alphalcm.infobip.com/"):
        # Initialize the KaceApi class with optional username, password, and URL
        self.api_username = kace_api_username
        self.api_password = kace_api_password
        self.cookies = None  # Will be populated during login process
        self.kace_url = kace_url
        self.login_to_kace()  # Automatically login upon initialization


    def __str__(self):  # For troubleshooting purposes, returns a string representation
        return f'\nAuth data report!\nAPI Username: {self.api_username}, password length: {len(self.api_password)} symbols.' \
               f'\nLength of cookies: {len(self.cookies) if self.cookies else 0}.'

    def login_to_kace(self):
        # Log in to KACE SMA API and obtain authentication cookies
        print(f'Logging in to KACE SMA API with username: {self.api_username}')
        url = f'{self.kace_url}ams/shared/api/security/login'

        payload = json.dumps({"userName": self.api_username, "password": self.api_password})
        headers = {
            'Accept': 'application/json',
            'x-dell-api-version': '12',
            'Content-Type': 'application/json'
        }

        try:
            # Send a POST request to the login URL with credentials
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()  # Check for HTTP request errors
            self.cookies = response.cookies  # Store authentication cookies
        except requests.exceptions.RequestException as e:
            print(f"HTTP Request Error: {e}")
        except json.JSONDecodeError as e:
            print(f"JSON Parsing Error: {e}")

    def get_laptops_all(self):
        # Retrieve a list of all laptops from the API
        print('Requesting the list of all laptops')
        url = f'{self.kace_url}api/inventory/machines/?paging=limit 1000'

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'x-dell-api-version': '12'
        }

        response = requests.request("GET", url, headers=headers, cookies=self.cookies)


        machine_list = json.loads(response.text)


        # Extract the "Name" and "Os_name" fields from the JSON data into list 
        filtered_data = [{"Name": machine["Name"], "Os_name": machine["Os_name"]} for machine in machine_list["Machines"]]

        # Initialize an empty dictionary to store the converted data
        self.all_laptops = {}

        # Iterate through the list and build the dictionary of the machines
        for item in filtered_data:
            name = item["Name"]
            os_name = item["Os_name"]
            self.all_laptops[name] = os_name
      
        return self.all_laptops #return all the laptops with os name and os version 