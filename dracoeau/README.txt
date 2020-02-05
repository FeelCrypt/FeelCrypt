- Pour récupérer les données concernant le cours du Bitcoin de sa création jusqu'à aujourd'hui, nous avons utilisé l'api cryptocompare
- L'API se trouve sur ce lien : "https://min-api.cryptocompare.com/"
- La documentation ici : "https://min-api.cryptocompare.com/documentation"

- L'API permet de récupérer les données de n'importe quel cryptomonnaie.

- Le programme s'appelle "get_chart_price_cryptocurrencies_csv.py" et se situe dans le dossier dracoeau
- Le programme permet de récupérer le cours d'une cryptomonnaie.
- Pour cela il suffit de faire appel à la fonction "get_csv_crypto_prices()"
- Cette fonction prend un paramètre optionnel qui est la devise (par défaut BTC)
- Changez ce paramètre pour récupérer le cours d'une autre crypto que le BTC
	-> Exemple : "get_csv_crypto_prices(currency="ETH")"

- Le programme renvoie un fichier csv dont le nom est "chart_price_{inserer_nom_crypto}.csv"

EXEMPLE D'UTILISATION : 

1) Créer un fichier "test.py" dans le même dossier (dracoeau)
2) Ouvrir le fichier avec n'importe quel éditeur de texte
3) Copiez ces lignes

# get bitcoin price in csv format

import get_chart_price_cryptocurrencies_csv

def main():
	get_chart_price_cryptocurrencies_csv.get_csv_crypto_prices('ETH')

if __name__ == "__main__":
	main()

4) cela vous renverra un csv contenant le cours de la crypto ETH.

5) changer le paramètre de get_csv_crypto_prices par la crypto de votre choix







