import os
import subprocess
import random
import time
import psutil

def get_nordvpn_credentials():
    """Retrieve VPN credentials from environment variables."""
    username = os.getenv("USER")
    password = os.getenv("PASS")
    if not username or not password:
        raise ValueError("VPN credentials are not set in environment variables.")
    return username, password

class OpenVPNManager:
   # def __init__(self, config_dir="C:/Users/FSuarezJimenez/dev/SocialDigest/.nordvpn_servers/"):
    def __init__(self, config_dir="./.nordvpn_servers/"):
        """
        Initialize the OpenVPN manager with the configuration directory.
        :param config_dir: Path to the folder containing VPN .ovpn configuration files starting with
        the 2 characters iso country code (e.g., "nl" for Netherlands).
        """
        self.config_dir = config_dir
        self.process = None  # Stores the OpenVPN process
        self.connected_country = None  # Stores the current connected country

    def _get_random_config(self, country_code):
        """
        Get a random .ovpn configuration file for a given country ISO code.
        :param country_code: 2-character ISO country code (e.g., "nl" for Netherlands).
        :return: Path to a random .ovpn file or None if not found.
        """
        country_code = country_code.lower()  # Ensure lowercase matching
        configs = [f for f in os.listdir(self.config_dir) if f.startswith(country_code) and f.endswith(".ovpn")]
        
        if not configs:
            print(f"No configuration files found for country code {country_code}.")
            return None
        
        return os.path.join(self.config_dir, random.choice(configs))
    
    def connect(self, country_code):
        """
        Connect to VPN using OpenVPN and a country-specific .ovpn file.
        :param country_code: 2-character ISO country code (lowercase expected).
        """
        config_path = self._get_random_config(country_code)

        if not config_path:
            return

        # Kill any existing OpenVPN process before starting a new one
        self.disconnect()

        self.server = config_path.split("/")[-1]    

        try:
            self.process = subprocess.Popen(
                ["openvpn", "--config", config_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
            time.sleep(10)  # Wait for connection to establish
            self.connected_country = country_code.lower()
            print(f"Connected to VPN ({self.connected_country.upper()}: {self.server}).")
        except Exception as e:
            print(f"Error connecting to VPN: {e}")

    def disconnect(self):
        """Disconnect from VPN."""
        try:
            for proc in psutil.process_iter():
                if proc.name() in ["openvpn.exe", "openvpn"]:
                    proc.terminate()
                    print(f"Disconnected from {self.server}")
                    break
            self.connected_country = None
        except Exception as e:
            print(f"Error disconnecting from VPN: {e}")

    def reconnect(self, new_country_code):
        """
        Reconnect to another country.
        :param new_country_code: 2-character ISO country code (lowercase expected).
        """
        print(f"Reconnecting to {new_country_code.upper()}...")
        self.connect(new_country_code)

    def status(self):
        """Check if the VPN is connected and display the country."""
        if self.connected_country:
            print(f"VPN is active. Connected to {self.connected_country.upper()}.")
        else:
            print("VPN is not connected.")

