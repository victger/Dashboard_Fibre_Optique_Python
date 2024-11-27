from driver.driver import driver, wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import requests
import os

def download_file():

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

    DIRECTORY = "data/deploiement_file"

    if not os.path.exists(DIRECTORY):
        os.makedirs(DIRECTORY)

    file_path = os.path.join(DIRECTORY, deploiement_file_name)

    response = requests.get(deploiement_url)

    if response.status_code == 200:
        with open(file_path, "wb") as file:
            file.write(response.content)
    else:
        print(f"Échec du téléchargement du fichier Excel de déploiement. Statut: {response.status_code}")

    communes_data_url= "https://perso.esiee.fr/~courivad/python_advanced/_downloads/8578d763bdb7d7d0d1a7aaeb2e3b4814/datagouv-communes.geojson"

    DIRECTORY = "data/communes_data"

    if not os.path.exists(DIRECTORY):
        os.makedirs(DIRECTORY)

    file_path = os.path.join(DIRECTORY, 'datagouv_communes.geojson')

    response = requests.get(communes_data_url)

    if response.status_code == 200:
        with open(file_path, "wb") as file:
            file.write(response.content)
    else:
        print(f"Échec du téléchargement du fichier GeoJSON des communes. Statut: {response.status_code}")