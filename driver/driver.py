from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

chrome_options = Options()

chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")  # For Docker
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-software-rasterizer")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'fr,fr_FR'})

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.set_window_size(1920, 1080)
wait = WebDriverWait(driver, 10)