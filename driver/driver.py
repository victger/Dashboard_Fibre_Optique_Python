from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Configuration des options Chrome
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Ouvrir en plein écran
chrome_options.add_argument("--disable-infobars")  # Désactiver les infobars
chrome_options.add_argument("--disable-extensions")  # Désactiver les extensions
chrome_options.add_argument("--incognito")  # Mode incognito

# Initialisation du ChromeDriver avec WebDriverManager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
wait = WebDriverWait(driver, 10)  # Attend jusqu'à 10 secondes