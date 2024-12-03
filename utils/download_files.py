from driver.driver import driver, wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utils.utils import download_from_url, setup_global_variables

def download_deploiement():

    URL= "https://www.data.gouv.fr/fr/datasets/le-marche-du-haut-et-tres-haut-debit-fixe-deploiements/"
    driver.get(URL)

    downloadable_files = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, "//div[contains(@data-v-ebceacca,'') and contains(@data-v-9b5f7714, '') and starts-with(@id, 'resource') and contains(@class,'border border-default-grey')]")
    ))

    for downloadable_file in downloadable_files:

        temp_title= downloadable_file.text.split('\n')[0]
        if "deploiement" in temp_title:
            deploiement_file_name= temp_title+".xlsx"
            deploiement_file= downloadable_file
            break

    deploiement_download_button= deploiement_file.find_element(By.XPATH, ".//a[@data-v-ebceacca='' and @title='Télécharger le fichier']")
    deploiement_url= deploiement_download_button.get_attribute('href')
    driver.quit()

    download_from_url(url= deploiement_url, input_dir='data/deploiement_file', output_name=deploiement_file_name)

def download_communes_data():

    communes_data_url= "https://perso.esiee.fr/~courivad/python_advanced/_downloads/8578d763bdb7d7d0d1a7aaeb2e3b4814/datagouv-communes.geojson"

    download_from_url(url= communes_data_url, input_dir='data/communes_data', output_name='datagouv_communes.geojson')

def download_files():
    
    download_deploiement()
    download_communes_data()
    setup_global_variables() # Could be improved. no real need to have global variables