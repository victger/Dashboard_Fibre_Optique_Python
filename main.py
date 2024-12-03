from utils.download_files import download_files
from utils.utils import process_data
from app.app import launch_app

download_files()

df_departement, df_region, df_commune, slider_dict = process_data()

launch_app(df_region, df_departement, df_commune, slider_dict)