***** Term Frequency - Inverse Document Frequency *****

L'objectif de la TF-IDF est de déterminer quels mots permettent de différencier un texte des autres au sein d'un corpus.

Nous avons étudié cette méthode pour voir si on pouvait réussir à extraire les commentaires Reddit les plus pertinents.

Le fonctionnement de cette méthode est résumé dans le fichier TF-IDF.ipynb qui est en fait l'exemple du site Towards Data Science.
Dans ce fichier se trouve le fonctionnement de base de la TF-IDF.

Le fichier TF-IDF Reddit_Raphael.ipynb effectue pour chaque csv (un csv correspond à une journée de commentaires Reddit):
    > Le nettoyage des commentaires avec des techniques de NLP
    > la TF-IDF de chaque csv

Cette méthode n'a pas donné de bons résultats : nous avons décider de l'abandonner
