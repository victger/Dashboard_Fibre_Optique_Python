from dash import Dash
from utils.download_file import download_file
from app.app import launch_app
from utils.utils import process_data

def main():
    
    download_file()

    df_departement, df_region, df_commune, slider_dict = process_data()

    launch_app(df_region, df_departement, df_commune, slider_dict)

if __name__ == "__main__":
    main()