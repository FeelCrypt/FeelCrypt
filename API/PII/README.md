I. Comment utiliser l'API ?

Dans l'archive dézippée du projet, l'API Django se trouve dans le dossier API/PII. 

Ouvrir PyCharm et ouvrir un nouvel environnement virtuel.
Dans cette environnement se placer dans le dossier API/PII

Tout d'abord il faut installer les librairies nécessaires à l'utilisation du projet :
	-> "pip install -r requirement.txt"

Pour lancer le scrapping en arrière plan des commentaires reddit (tts les 2 heures automatiquement)
	-> lancer "python manage.py migrate django_cron" puis "python manage.py runcrons"
Ensuite, pour lancer l'API sur le serveur local, "python manage.py runserver"
On peut accéder au serveur web avec "127.0.0.1:8000" et accéder à la prédiction du jour

