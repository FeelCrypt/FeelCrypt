# API

Ce projet utilise python 3.7

## Installation Packages

Avant de pouvoir lancer l'API, il faut installer les package nécessaire sur la machine.
Pour cela, il suffit d'ouvrir une console dans le dossier PII, où se situe le fichier _requirements.txt_ et de lancer la commande:

```
pip install -r requirements.txt
```

## Lancement de l'API

Pour que l'API fonctionne correctement, il faut lancer les cronjobs ainsi que le serveur en lui même

### Lancement des Cron Jobs

Dans le dossier PII, où se trouve le fichier _manage.py_, lancer cette commande:

```
python manage.py runcrons
```

### Lancement du serveur Django

Dans le même dossier, lancer la commander:

```
python manage.py runserver
```
