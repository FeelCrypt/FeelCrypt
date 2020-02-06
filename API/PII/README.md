# Comment utiliser l'API ?

Dans l'archive dézippée du projet, l'API Django se trouve dans le dossier API/PII. 

Ouvrir PyCharm et ouvrir un nouvel environnement virtuel.
Dans cette environnement se placer dans le dossier API/PII

Tout d'abord il faut installer les librairies nécessaires à l'utilisation du projet :
'''bash
pip install -r requirement.txt
'''

# Scraping en arrière plan

Pour lancer le scrapping en arrière plan des commentaires reddit (tts les 2 heures automatiquement)
Lancer la commande :
'''bash
python manage.py migrate django_cron
'''

Puis lancer :
'''bash
python manage.py runcrons
'''

# Lancement du serveur 

Ensuite, pour lancer l'API sur le serveur local :
'''bash
python manage.py runserver
'''

On peut accéder au serveur web en tapant dans la barre de recherche :
'''bash
127.0.0.1:8000
'''

On accède ensuite à la prédiction du jour
