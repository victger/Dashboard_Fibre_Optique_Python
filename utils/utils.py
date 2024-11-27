import pandas as pd
import unidecode
from pathlib import Path
import math
import os
import re
import sys

DATA_PATH= os.path.join("data","deploiement_file")
FILE= os.listdir(DATA_PATH)[0]
FILE_PATH= os.path.join(DATA_PATH,FILE)

LAST_YEAR= FILE[:4]
LAST_QUARTER= FILE[4:6]
LAST_PERIOD= LAST_QUARTER+' '+LAST_YEAR

def generate_periods():
    periods = ['T4 2017']
    
    current_year = 2017
    current_quarter = 4
    
    last_quarter, last_year = LAST_PERIOD.split()
    last_quarter = int(last_quarter[1])
    last_year = int(last_year)
    
    while (current_year < last_year) or (current_year == last_year and current_quarter < last_quarter):
        current_quarter += 1
        
        if current_quarter > 4:
            current_quarter = 1
            current_year += 1
        
        periods.append(f'T{current_quarter} {current_year}')
    
    return periods

def round_decimals_down(number:float, decimals:int=2):
    """
    Returns a value rounded down to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more")
    elif decimals == 0:
        return math.floor(number)

    factor = 10 ** decimals
    return math.floor(number * factor) / factor

def round_decimals_up(number:float, decimals:int=2):
    """
    Returns a value rounded up to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more")
    elif decimals == 0:
        return math.ceil(number)

    factor = 10 ** decimals
    return math.ceil(number * factor) / factor

def normalize_columns(df):
    """
    Normalise les noms des colonnes de la dataframe

    Args :
        df : dataframe lue

    Return :
        df : dataframe dont les noms de colonne sont normalisés
    """

    old_columns = df.columns.values
    new_columns = [unidecode.unidecode(re.sub(r'\s+', ' ', i).strip().replace(' ', '_').lower()) for i in old_columns]
    d = dict(zip(old_columns, new_columns))
    df = df.rename(columns=d)

    return df

def to_long(df, vars):
    """
    Transorme une dataframe au format large en format long. On sépare les colonnes concernant les périodes
    pour les mettre en ligne (voir csv originaux) pour mieux visualiser.

    Args :
        df : dataframe concernée
        vars: colonnes qui servent de pivot, elles ne changent pas

    Return :
        df : dataframe au format long
    """

    df= pd.melt(df, vars, var_name= 'annee', value_name= 'nombre_de_logements_raccordables')

    annee= []
    trimestre= []
    for element in df["annee"].str.split("_"):
        annee+=[element[1]]
        trimestre+= [element[0][1]]
    df["annee"]= annee
    df["trimestre"]= trimestre

    return df

def nettoyage(zone):
    """
    Nettoie une dataframe en appelant les fonctions précédemment créées.

    Args :
        zone: Nom (sans l'extension) du fichier csv à nettoyer

    """
    df = pd.read_excel(FILE_PATH, sheet_name=zone, skiprows=4)
    df= normalize_columns(df)
    
    tab_col= ['nombre_locaux_ipe_'+LAST_QUARTER.lower()+'_'+LAST_YEAR+'_(somme_tous_oi)', 'code_region', 'logements', 'etablissements'] # Colonnes inutiles
    vars= ['nom_'+unidecode.unidecode(zone).lower()[:-1], 'meilleure_estimation_des_locaux_'+LAST_QUARTER.lower()+'_'+LAST_YEAR] #Colonnes faisant pivot à la transformation en wide to long
    col_ordre= ["code_"+unidecode.unidecode(zone).lower()[:-1], "nom_"+unidecode.unidecode(zone).lower()[:-1], "meilleure_estimation_des_locaux_"+LAST_QUARTER.lower()+"_"+LAST_YEAR, "annee", "trimestre", "nombre_de_logements_raccordables"] #Ordre final des colonnes de la df

    if zone=='Régions':
        tab_lig= [i for i in range(8)]

    elif zone=='Départements':
        tab_lig= [index for index in df.index if str(df.iloc[index]['code_departement']).startswith("97")] # On supprime les outre-mers
        vars+= ['code_departement']

    elif zone=='Communes':
        tab_col+= ['code_departement', 'siren_epci_'+LAST_YEAR, 'epci_amii', 'source_retenue_'+LAST_QUARTER.lower()+'_'+LAST_YEAR, 'engagements_l._33-13_(amii_et_amel)', 'intentions_privees_hors_engagement_l._33-13', 'oi_'+LAST_QUARTER.lower()+'_'+LAST_YEAR, 'commune_rurale', 'commune_de_montagne', 'zones_tres_denses']
        tab_lig= [index for index in df.index if str(df.iloc[index]['code_commune']).startswith("97")] # On supprime les outre-mers
        vars+= ['code_commune']

    df= df.drop(tab_col, axis= 1)
    df= df.drop(tab_lig, axis= 0)
    df= to_long(df, vars)
    df=df.reindex(columns=col_ordre)

    df['annee'] = pd.to_numeric(df['annee'], errors='coerce')
    df['trimestre'] = pd.to_numeric(df['trimestre'], errors='coerce')

    return df

def process_data():

    df_region = nettoyage('Régions')
    df_departement = nettoyage('Départements')
    df_commune = nettoyage('Communes')

    df_departement["proportion_de_logements_raccordables"]= df_departement["nombre_de_logements_raccordables"]/df_departement["meilleure_estimation_des_locaux_"+LAST_QUARTER.lower()+'_'+LAST_YEAR]
    df_departement["classe"]= [str(round_decimals_down(element, 1))+" - "+str(round_decimals_up(element, 1)) for element in df_departement["proportion_de_logements_raccordables"]]
    df_departement= df_departement.sort_values(by=['classe'])
    tri_an= generate_periods()
    key= [i for i in range(len(tri_an))]
    d= dict(zip(key, tri_an)) # For slider

    periode= ["T"+ str(df_region["trimestre"].iloc[index])+" "+str(df_region["annee"].iloc[index]) for index in df_region.index]# On récupère la période avec de l'algorithmique
    df_region["periode"]= periode
    df_region["proportion_de_logements_raccordables"]= df_region["nombre_de_logements_raccordables"]/df_region["meilleure_estimation_des_locaux_"+LAST_QUARTER.lower()+'_'+LAST_YEAR]

    df_commune= df_commune[df_commune["trimestre"]==int(LAST_QUARTER[-1])]
    df_commune= df_commune[df_commune["annee"]==int(LAST_YEAR)]
    df_commune["proportion_de_logements_raccordables_dans_la_commune"]= df_commune["nombre_de_logements_raccordables"]/df_commune["meilleure_estimation_des_locaux_"+LAST_QUARTER.lower()+'_'+LAST_YEAR]
    
    return df_departement, df_region, df_commune, d

def period_to_str():

    return f'{LAST_QUARTER[-1]}ème trimestre de {LAST_YEAR}'