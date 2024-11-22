import pandas as pd
import unidecode
from pathlib import Path
import math
import os
import sys

# Diverses fonctions utiles

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

def lecture_csv(zone):
    """
    Lit un fichier csv extrait du fichier Excel original

    Args :
        zone: Nom (sans extension) du fichier csv concerné

    Return :
        df : dataframe lue
    """

    DATA_PATH= "data/"
    FILE_PATH= os.path.join(DATA_PATH,"2022t2-obs-hd-thd-deploiement-vf.xlsx")
    read_file = pd.read_excel(FILE_PATH, sheet_name=zone)
    read_file.to_csv(os.path.join(DATA_PATH,zone+'.csv'), index= False, header=True)
    df= pd.read_csv(os.path.join(DATA_PATH,zone)+'.csv', sep=",", skiprows=lambda x: x in range(0,4), low_memory=False)

    return df

def normalise(df):
    """
    Normalise les noms des colonnes de la dataframe

    Args :
        df : dataframe lue

    Return :
        df : dataframe dont les noms de colonne sont normalisés
    """

    old_columns= df.columns.values
    new_columns = [unidecode.unidecode(i.strip().replace(' ', '_').lower()) for i in old_columns]
    d= dict(zip(old_columns, new_columns))
    df= df.rename(columns= d)

    return df

def sup_col_ou_l(df, tab, paxis):
    """
    Supprime les colonnes ou les lignes d'une dataframe

    Args :
        df : dataframe concernée
        tab: tableau du nom des colonnes à supprimer
        paxis: 0 pour supprimer des lignes, 1 pour supprimer des colonnes

    Return :
        df : dataframe avec les colonnes ou lignes supprimées
    """

    if paxis==1:
        df= df.drop(tab, axis=1) #Colonne
    else:
        df= df.drop(tab) #Ligne
    
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

def change_col_ordre(df, tab):
    """
    Change l'ordre des colonnes d'une dataframe

    Args :
        df : dataframe concernée
        tab: tableau contenant l'ordre des colonnes

    Return :
        df : dataframe dont les colonnes ont été ordonnées
    """

    df=df.reindex(columns=tab)

    return df

def nettoyage(zone):
    """
    Nettoie une dataframe en appelant fonctions précédemment créées.

    Args :
        zone: Nom (sans l'extension) du fichier csv à nettoyer

    """

    df= lecture_csv(zone)
    df= normalise(df)
    
    tab_col= ['nombre_locaux_ipe_t2_2022_(somme_tous_oi)', 'code_region', 'logements', 'etablissements'] # Colonnes inutiles
    vars= ['nom_'+unidecode.unidecode(zone).lower()[:-1], 'meilleure_estimation_des_locaux_t2_2022'] #Colonnes faisant pivot à la transformation en wide to long
    col_ordre= ["code_"+unidecode.unidecode(zone).lower()[:-1], "nom_"+unidecode.unidecode(zone).lower()[:-1], "meilleure_estimation_des_locaux_t2_2022", "annee", "trimestre", "nombre_de_logements_raccordables"] #Ordre final des colonnes de la df

    if zone=='Régions':
        tab_lig= [i for i in range(8)] # On supprimes les outre-mers

    elif zone=='Départements':
        tab_lig= [index for index in df.index if str(df.iloc[index]['code_departement']).startswith("97")] # On supprime les outre-mers
        vars+= ['code_departement']

    elif zone=='Communes':
        tab_col+= ['code_departement', 'siren_epci', 'epci_amii', 'source_retenue_t2_2022', 'engagements_l._33-13_et_amel', 'intentions_privees_hors_engagement_l._33-13', 'oi_t2_2022', 'commune_rurale', 'commune_de_montagne', 'zones_tres_denses']
        tab_lig= [index for index in df.index if str(df.iloc[index]['code_commune']).startswith("97")] # On supprime les outre-mers
        vars+= ['code_commune']

    df= sup_col_ou_l(df, tab_col, 1)
    df= sup_col_ou_l(df, tab_lig, 0)
    df= to_long(df, vars)
    df= change_col_ordre(df, col_ordre)

    df['annee'] = pd.to_numeric(df['annee'], errors='coerce')  # Convertir en entier, NaN pour les erreurs
    df['trimestre'] = pd.to_numeric(df['trimestre'], errors='coerce')  # Convertir en entier, NaN pour les erreurs

    return df

def process_data(df_departement, df_region, df_commune):   

    df_departement["proportion_de_logements_raccordables"]= df_departement["nombre_de_logements_raccordables"]/df_departement["meilleure_estimation_des_locaux_t2_2022"]
    df_departement["classe"]= [str(round_decimals_down(element, 1))+" - "+str(round_decimals_up(element, 1)) for element in df_departement["proportion_de_logements_raccordables"]]
    df_departement= df_departement.sort_values(by=['classe'])
    tri_an= ['T4 2017', 'T1 2018', 'T2 2018', 'T3 2018', 'T4 2018', 'T1 2019', 'T2 2019', 'T3 2019', 'T4 2019', 'T1 2020', 'T2 2020', 'T3 2020', 'T4 2020', 'T1 2021', 'T2 2021', 'T3 2021', 'T4 2021', 'T1 2022', 'T2 2022']
    key= [i for i in range(len(tri_an))]
    d= dict(zip(key, tri_an)) # Sert au slider

    periode= ["T"+ str(df_region["trimestre"].iloc[index])+" "+str(df_region["annee"].iloc[index]) for index in df_region.index]# On récupère la période avec de l'algorithmique
    df_region["periode"]= periode
    df_region["proportion_de_logements_raccordables"]= df_region["nombre_de_logements_raccordables"]/df_region["meilleure_estimation_des_locaux_t2_2022"]

    df_commune= df_commune[df_commune["trimestre"]==2]
    df_commune= df_commune[df_commune["annee"]==2022] # Pour notre carte, on fixe au 2ème trimestre de 2022
    df_commune["proportion_de_logements_raccordables_dans_la_commune"]= df_commune["nombre_de_logements_raccordables"]/df_commune["meilleure_estimation_des_locaux_t2_2022"]

    return df_departement, df_region, df_commune, d