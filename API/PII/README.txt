I. Comment utiliser l'API ?

Dans l'archive d�zipp�e du projet, l'API Django se trouve dans le dossier API/PII. 

Ouvrir PyCharm et ouvrir un nouvel environnement virtuel.
Dans cette environnement se placer dans le dossier API/PII

Tout d'abord il faut installer les librairies n�cessaires � l'utilisation du projet :
	-> "pip install -r requirement.txt"

Pour lancer le scrapping en arri�re plan des commentaires reddit (tts les 2 heures automatiquement)
	-> lancer "python manage.py migrate django_cron" puis "python manage.py runcrons"
Ensuite, pour lancer l'API sur le serveur local, "python manage.py runserver"
On peut acc�der au serveur web avec "127.0.0.1:8000" et acc�der � la pr�diction du jour
















