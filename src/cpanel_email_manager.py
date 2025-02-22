import requests
import os

class CPanelEmailManager:
    """
    Class to manage email addresses and accounts using the cPanel API
    """

    def __init__(self):
        """
        Initialize the EmailManager class
        """
        self.api_token = os.getenv("CPANEL_TOKEN")
        self.domain = os.getenv("CPANEL_URL")
        self.cpanel_url = f"https://{self.domain}:2083/execute/Email/add_pop"
        self.headers = {
            "Authorization": f"cpanel xastrinc:{self.api_token}"
        }

    def create_email_address(self,email_user,password, quota=10):
        """
        Create an email address using the cPanel API

        Parameters:
        email_user (str): The local part of the email address (e.g. user)
        password (str): The password for the email address
        quota (int): The quota for the email address (default: 10)

        Returns:
        dict: The response from the cPanel API

        Raises:
        requests.exceptions.SSLError: If there is an SSL certificate error
        requests.exceptions.RequestException: If there is a request error
        """
        params = {
            "email": email_user,
            "domain": 'xastrin.com',
            "password": password,
            "quota": quota
        }
        #response = requests.get(self.cpanel_url, headers=self.headers, params=params, verify=False)
        try:
            # Verify SSL certificate by default (Good practice)
            response = requests.get(self.cpanel_url, headers=self.headers, params=params)

            # Raise an error for non-200 responses
            response.raise_for_status()
            print(response.json())  # Print the response (check for errors)
        except requests.exceptions.SSLError as e:
            print("SSL error: Check your certificate settings.", e)

        except requests.exceptions.RequestException as e:
            print("Request error:", e)