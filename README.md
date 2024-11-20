
# Projet Dashboard Python

  

Voici le projet de dashboard réalisé en Python par Victor GERARD et Zakary BELKACEM dans le cadre de nos études à l'ESIEE Paris. Les données ici présentées sont relatives aux raccordements de la fibre en France métropolitaine aux niveaux communal, départemental et régional.

Les données utilisées sont issues du gouvernement et consultables à l'adresse:

https://static.data.gouv.fr/resources/le-marche-du-haut-et-tres-haut-debit-fixe-deploiements/20221013-173531/2022t2-obs-hd-thd-deploiement-vf.xlsx

Des données de géolocalisation ont aussi été utilisées et téléchargeables à l'adresse: https://perso.esiee.fr/~courivad/python_advanced/_downloads/8578d763bdb7d7d0d1a7aaeb2e3b4814/datagouv-communes.geojson

  

Description de certaines colonnes après traitement du tableau Excel:

  

- meilleure_estimation_des_locaux_t2_2022: Estimation du nombre de logements au 2ème trimestre de 2022 dans une zone donnée.

- nombre_de_logements_raccordables: Nombre de logements pouvant être fibrés dans une zone donnée.

  

Dans le cadre de notre étude, nous avons utilisé la colonne "meilleure_estimation_des_locaux_t2_2022" pour d'autres périodes que celle mentionnée à des fins statistiques. En effet, nous considérons que dans une commune, un département ou une région, le nombre de logements varie de manière négligeable entre 2017 et 2022. Cela nous permettra d'illustrer efficacement divers phénomènes.

  

# User Guide

  

Pour télécharger notre projet, il est nécessaire de le clôner en tapant l'instruction:

  

    git clone https://git.esiee.fr/belkacez/dashboard_python.git

  

Pour commencer, il est nécessaire d'installer les packages présents dans le fichier requirements.txt avec la ligne de commande python suivante une fois dans le dossier approprié:

    -m pip install -r requirements.txt 

On s'assure alors que les fichiers suivants soient dans le même dossier:

  

- 2022t2-obs-hd-thd-deploiement-vf.xls

- app.py

- datagouv-communes.geojson

- README.md

- requirements.txt

  

On procède comme suit pour accéder au Dashboard :

  

- Accéder au dossier téléchargé dans un terminal

- Dans le terminal, exécutez la ligne de commandes: python app.py

## Temps de chargement

Attention ! Le script prend du temps à être exécuté (environ 1 minute pour un PC relativement puissant). Une fois l'exécution terminée, cliquer sur l'adresse retournée par le terminal. On a alors accès au Dashboard une fois la page chargée. On notera que le carte peut prendre quelque temps à apparaître, en général moins de 2 minutes. Cela est dû au long traitement à effectuer.

  
  

# Rapport d'analyse du Dashboard

  

Rapport d'analyse des données afffichées dans le dashboard:

  

Les graphes tracés dans notre Dashboard illustrent différents phénomènes.

  

Premièrement, notre histogramme nous fait réaliser que la proportion de logements raccordables en France métropolitaine a très fortement augmenté pour tous les départements entre le 1er trimestre de 2017 et le 2ème trimestre de 2022. Celle-ci est très marquante lorsque l'on passe dicrement du début à la fin de cette période puisqu'en fin 2017, seuls 2 départements ont une propotion d'accès supérieure à la moitié tandis qu'à la mi-2022, ils sont au nombre de 79. On peut constater par ailleurs que les départements de province sont ceux qui ont eu la plus forte évolution, laissant penser qu'il existe une forte inégalité d'accès à la fibre à en France métropolitaine.

  

Le second graphe est encore plus parlant. En effet, on trace cette fois-ci l'évolution de la proportion de logements raccordables dans une région donnée, toujours en France métropolitaine. Ce graphe confirme la forte disparité d'accès à la fibre dans notre pays car au 4ème trimestre de 2017, la proportion de logements raccordables en Ile-de-France domine largement celle des autres régions. Néanmoins, ces dernières tendent à rattraper l'accès à la fibre en Ile-de-France au 2ème trimestre de 2022, réduisant fortement les ingéalités d'accès à la fibre en France métropolitaine.

  

Notre dernier graphe présente visuellement le contraste entre les différentes communes de France métropolitaine concernant l'accès à la fibre. La première élément frappant à vue d'oeil est "l'aglutinnement" des couleurs. En effet, les communes où la proportion de logements raccordables est faible sont généralement collés, idem pour les communes où la proportion de logements raccordables est élevée. Cela met donc en évidence la disparité d'accès à la fibre en France métropolitaine et révèle que l'accès semble plus facile autour des grosses métropoles, contrairement aux zones reculées. On peut d'ailleurs deviner la "diagonale du vide" en jaune clair, qui s'étend des Meuses aux Landes.

  

Au terme de cette étude, on en déduit que l'accès à la fibre en France métropolitaine est flagrant à toutes les échelles. Néanmoins, on constate une accélération du déploiement de la fibre en France métropolitaine.

  

# Developer Guide

  

Le dashboard est fonctionnel grâce à un unique fichier Python, divisé lui-même en plusieurs parties:

  

- La première contient diverses fonctions utiles au nettoyage des données et à la création d'un fichier csv final, qui permet à tout utilisateur disposant de notre dossier de réexploiter directement les données nettoyées, ou de les visualiser simplement. Nous uniformisons alors le nom des colonnes, respectons les normes de format des dataframes (long), changeons l'ordre des colonnes et supprimons les colonnes inutiles. On supprime également les données concernant les outre-mer, qui ne font pas partie de notre étude.

  

- La deuxième concerne directement le nettoyage des données mais aussi la génération de nouvelles données qui seront utiles pour notre dashboard. Celles-ci ne sont pas inclues dans les fichiers csv finaux pour bien faire la distinction entre les données originales et le traitement de ces données.

  

- La troisième et dernière partie concerne la création du dashboard et des graphes le concernant. Nous utilisons Dash qui reprend des notions de code HTML, permettant alors de structurer notre Dashboard.