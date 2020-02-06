# Cours Bitcoin 

Ce programme permet de récupérer le cours d'une cryptomonnaie sous forme de fichier csv à l'aide de l'api cryptocompare

L'API se trouve sur ce lien :

'''bash
https://min-api.cryptocompare.com/
'''

La documentation ici : 

'''bash
https://min-api.cryptocompare.com/documentation
'''

# Utilisation

L'API permet de récupérer les données de n'importe quel cryptomonnaie.
Le programme s'appelle "get_chart_price_cryptocurrencies_csv.py" et se situe dans le dossier dracoeau
Le programme permet de récupérer le cours d'une cryptomonnaie.

Pour cela il suffit de faire appel à la fonction :
'''bash
get_csv_crypto_prices()
'''

Cette fonction prend un paramètre optionnel qui est la devise (par défaut BTC)
Changez ce paramètre pour récupérer le cours d'une autre crypto que le BTC

Exemple : 
'''bash
get_csv_crypto_prices(currency="ETH")
'''

Le programme renvoie un fichier csv dont le nom est :
'''bash
chart_price_{inserer_nom_crypto}.csv
'''
