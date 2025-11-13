# driver_setup.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os


def setup_driver():
    """Initialize Chrome WebDriver using webdriver-manager + real Chrome profile."""

    options = Options()

    # Use your real logged-in Chrome profile to bypass login
    options.add_argument(r"user-data-dir=C:\Users\ext-Dakshak\AppData\Local\Google\Chrome\User Data\Profile 1")
    options.add_argument("profile-directory=Default")  # Change to "Profile 1" if needed

    # Stability & performance flags
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--start-maximized")
    options.add_argument("--remote-debugging-port=9222")

    # Hide automation warning
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    options.add_argument("--disable-blink-features=AutomationControlled")


    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=options)
    return driver
