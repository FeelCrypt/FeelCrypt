import praw               # API pour reddit
import pandas as pd       # pour afficher les dictionnaires sous forme de tableaux
import datetime as dt     # Pour convertir la date au bon format
import os
import sys
import shutil

reddit = praw.Reddit(client_id='BEjar6X3GYV5Vw', \
                     client_secret='lg6D6DXG14FH4kHtGVt7cins5OY', \
                     user_agent='feelcrypt', \
                     username='feelcrypt', \
                     password='spiderminute38')

# Variables de configuration globale
nb_top_posts = 500  # nombre de posts selectionnés parmi les premiers (limite = 500)
subreddit_title = 'bitcoin' # Subreddit bitcoin
subreddit_title2 = 'btc' # Subreddit btc

# Variables globales

scrap_all_comments = True
# Si false : prend seulement les 32 premiers commentaires de chaque post
# Si true : prend tous les commentaires du post

scrap_responses_to_comments = True
# Si false : ne prend que les réponses directes au post
# Si true : prend également en compte les réponses aux commentaires

# Fonctions
def get_script_dir_path():
    script_dir_path = './' 
    script_dir_path += '\\'
    return script_dir_path

# Vérifier si le dossier passé en paramètre (+chemin relatif au dossier du subreddit) existe, sinon le créer
def create_folder(subreddit_path, folder_name):
    folder_name = folder_name
    folder_path = subreddit_path + folder_name + '\\'
    try:
        os.makedirs(folder_path)
        print('Dossier créé : ' + folder_name) # Log
    except FileExistsError:
        print('Dossier déjà existant : ' + folder_name) # Log
        pass
    return folder_path

# Créer la liste des id des posts à traiter
def create_id_todo(subreddit_path):
    # Créer la variable sur le subreddit
    subreddit = reddit.subreddit(subreddit_title)
    
    # Récupérer les n premiers posts de notre subreddit de notre liste
    top_posts = []

    for post in subreddit.new(limit = nb_top_posts):
        top_posts.append(post)

    # Enregistrer les id dans une liste
    top_posts_id = []
    for post in top_posts:
        top_posts_id.append(post.id)

    # Enregistrer la liste des id dans un fichier txt

    # Créer le chemin de la liste d'id à traiter
    file_name = 'id_todo.txt'
    id_todo__path = subreddit_path + file_name

    # Remplir la liste avec les id
    top_posts_id_file = open(id_todo__path,'w')
    for post_id in top_posts_id:
         top_posts_id_file.write(post_id)
         top_posts_id_file.write('\n')
    top_posts_id_file.close()
    
    # Log
    print('Fichier initialisé : ' + file_name)
    
    return id_todo__path

# Créer le fichier pour compter le nombre de commentaires total
# Le créer et l'initialiser à 0 (ecrase et remplace par 0 si le fichier existe déjà)
def create_counter(subreddit_path):
    file_name = 'total_comments_counter.txt'
    counter__path = subreddit_path + file_name
    nb_file = open(counter__path,'w').close()
    nb_file = open(counter__path,'w')
    nb_file.write(str(0))
    nb_file.close()
    
    # log
    print('Fichier initialisé : ' + file_name)
    
    return counter__path

def create_csv(subreddit_path, file_name):
    # assemble path
    full_path = subreddit_path + file_name
    # Check if it exists
    csv_exists = os.path.exists(full_path.replace(os.sep, '/'))
    
    if (not csv_exists):
        print(file_name + " does not exists >> initializing empty csv")
        with open(full_path, "w") as my_empty_csv:
            pass
    else:
        print(file_name + " already exists")

# Functions
# Fonction de conversion pour la date avec timestamp
def get_date(created):
    return dt.date.fromtimestamp(created)

# Ajouter le nb de commentaires traités dans le compteur
def updating_counter(counter_path, nb_comments, current_post_id):
        nb_file = open(counter_path,'r')
        total_comments = int(nb_file.read())
        print("previously total number of comments : " + str (total_comments))
        total_comments += nb_comments
        nb_file.close()
        nb_file = open(counter_path,'w').close()
        nb_file = open(counter_path,'w')
        nb_file.write(str(total_comments))
        nb_file.close()
        
        print(str(nb_comments) + " new comments scrapped from post " + str(current_post_id))
        print('total comments saved = ' + str(total_comments))

# Compter le nombre de lignes dans un fichier
def file_len(fname):
    i = 0
    with open(fname) as f:
        for l in enumerate(f):
            i += 1
    return i

# Compter le nombre de commentaires déjà scrapés pour un post
#def count_already_scrapped_comments(post_id)

# Récupérer la liste des commentaires déjà traités depuis le comment_manager
# Et comparer avec la liste récupérée

# Traiter chaque id du fichier todo
def get_comments(id_todo, comments_manager_id_path, comments_manager_counter_path, id_todo_path, comments_path, counter_path, subreddit_path):
    while id_todo:  # Vérifier si la liste n'est pas vide

        # Récupérer le post
        post = reddit.submission(id = id_todo[0])
        current_post_id = post.id[0:6]
        print('-----------------------------------\n\n')
        print('Starting working on post : ' + str(current_post_id))
        
        # initialiser le fichier txt pour les commentaires déjà traités, (ne change rien si le fichier existe déjà)
        print("Step 1 ---- initialise txt file for done comments")
        manager_file_path = comments_manager_id_path + str(current_post_id) + '.txt'
        comment_manager_file = open(manager_file_path,'a')
        comment_manager_file.close()
        
        ## Comparer le nb de commentaire actuel du pos à celui enregistré
        print("Step 2 ---- compare comments number on post")
        #nb_comments_done = file_len(manager_file_path) # old version
        current_nb_comments = post.num_comments # nb of comments right now on the post
        print("    Current number of comments on post : " + str(current_nb_comments))
        
        df_counter = pd.read_csv(comments_manager_counter_path, sep=';', names =['id','counter'])
        matching_line = df_counter[df_counter['id'].str.match(post.id)]
        id_exist = not matching_line.empty
        
        to_scrap = True # boolean to know if we have to scrap this post
        post_already_scrapped = False
        
        if(id_exist):
            print('    This post was scrapped before')
            
            # index of matching line 
            line_index = matching_line.index[0]
            
            # saved counter
            saved_counter = df_counter['counter'][line_index]
            print("    Saved counter of comments on post : " + str(saved_counter))
            
            # compare saved and current counter
            to_scrap = not (saved_counter == current_nb_comments)

            # replacing counter with current counter
            df_counter.at[line_index, 'counter'] = current_nb_comments
            
            post_already_scrapped = True
            
        else: # if we could not find the id in the csv
            # add the id and counter to csv
            df_counter = df_counter.append({'id':current_post_id,'counter':current_nb_comments}, ignore_index=True)
        
            # change booleans
            to_scrap = True
            post_already_scrapped = False
            print('    This post was not scrapped before')
        # Saving the new counter csv    
        df_counter.to_csv(comments_manager_counter_path, ';', mode='w', index=False, header=False) 
        
        print('    Do we have to scrap this post ? : ' + str(to_scrap))
        
        
        # If there are new comments to scrap
        if to_scrap:
            
            ## Récupérer les commentaires du poste
        
            #Réinitialiser le dictionnaire
            comments_dict = { "created_utc":[], \
                             "body":[], \
                             "score":[], \
                             "nb_replies":[], \
                             "stickied":[], \
                             "author":[], \
                             "id":[], \
                             "post_title":[], \
                             "post_id":[], \
                             "post_link":[]} 


            print("Step 4 ---- Se débarasser récursivement de la limite de 32 commentaires par requête")
            # Se débarasser récursivement de la limite de 32 commentaires par requête
            # NB : Cette partie est la plus longue lorsqu'on scrap un post
            if scrap_all_comments:
                post.comments.replace_more(limit=None)  # prendre en compte les commentaires supp
            else:
                post.comments.replace_more(limit=0)    # ignorer les commentaires supp

            print("Step 5 ---- Récupérer la liste des commentaires")
            # Récupérer la liste des commentaires
            if scrap_responses_to_comments:
                comments_list = post.comments.list()
            else:
                comments_list = post.comments

            # Remplir le dictionnaire de commentaires avec seulement les nouveaux commentaires
            # On check donc si le commentaire n'est pas dans la liste comment_manager_file
            # Réouvrir le fichier des commentaires          
            new_comments_list = []
                      
            for comment in comments_list:
                bool_comment_scrapped = False
                
                comment_manager_file = open(manager_file_path,'r')
                for comment_id_done in comment_manager_file:
                    if(str(comment.id) == str(comment_id_done[0:7])):
                        bool_comment_scrapped = True
                comment_manager_file.close()
                if not bool_comment_scrapped: # Si le commentaire n'avait pas été scrappé, le rajouter à la liste des commentaires scrappés
                    new_comments_list.append(comment)
                
            comment_manager_file = open(manager_file_path,'a')    
            for comment in new_comments_list:
                #print("--- this is a comment id from the new_comment_list : " + str(comment.id))
                origin_post = comment.submission
                comments_dict["created_utc"].append(comment.created_utc)
                comments_dict["body"].append(comment.body)
                comments_dict["score"].append(comment.score)
                comments_dict["nb_replies"].append(len(comment.replies))
                comments_dict["stickied"].append(comment.stickied)
                comments_dict["author"].append(comment.author)
                comments_dict["id"].append(comment.id)
                comments_dict["post_title"].append(origin_post.title)
                comments_dict["post_id"].append(origin_post.id)
                comments_dict["post_link"].append(origin_post.url)

                # Ajouter l'id du commentaires à la liste des commentaires scrappés
                comment_manager_file.write(comment.id + '\n')

            # mettre la data au format pandas (qui permet de faire un "tableur" à partir du dictionnaire)
            comments_data = pd.DataFrame(comments_dict)

            # Créer la liste des dates converties et la sauvgarder dans la variable _timstamp
            # created_utc est la colonne contenant les dates au mauvais format
            _timestamp = comments_data["created_utc"].apply(get_date)

            # ajouter la liste à une nouvelle colonne appelée timestamp
            comments_data = comments_data.assign(date = _timestamp)

            # Supprimer la colonne du temps inutile
            comments_data = comments_data.drop(columns="created_utc")

            # Déplacer la date en première position
            colonnes = comments_data.columns.tolist()
            colonnes = colonnes[-1:] + colonnes[:-1]
            comments_data = comments_data[colonnes]

            # Trier par la colonne date
            comments_sorted = comments_data.sort_values(by=['date'])

            ## Extraire plusieurs dataframe qui représentent chacun une date avec tous les commentaires dedans
            # Récupérer la liste des dates et indexer par dates
            comments_sorted.set_index(keys=['date'], drop=False,inplace=True)
            dates = comments_sorted['date'].unique().tolist()

            # Enregistrer dans une liste contenant chaque dataframe (1 data frame = 1 date)
            comments_splitperday = []
            for date in dates:
                comments_per_day = pd.DataFrame(comments_sorted.loc[comments_sorted.date == date])
                comments_splitperday.append(comments_per_day)

            # Enregistrer chaque dataframe dans un fichier csv
            for dataframe in comments_splitperday:
                # Récupérer la date du dataframe supprimer la colonne date
                date = str(dataframe.date.iloc[0])
                dataframe = dataframe.drop(columns="date")
                csv_path = comments_path + date + '.csv'

                # Check if file is empty (used to sed header or not)
                csv_exists = os.path.exists(csv_path.replace(os.sep, '/'))

                # Enregistrer au format csv avec pour nom la date
                dataframe.to_csv(csv_path, ';', mode='a', index=False, header= not csv_exists) 
                
                #----- Fin du traitement des commentaires d'un post d'un post

            # Retirer le premier id de la liste, le laisser à la fin, si le while est interrompu, il sera retiré alors que le post n'aura pas été traité
            id_todo.pop(0)

            # Ajouter l'id du post lu dans la liste des id_done si le post n'avait pas déjà été scrappé
            if (post_already_scrapped):
                id_done_path = subreddit_path + "id_done.txt"
                with open(id_done_path, "a") as file:
                    file.write(current_post_id)

            # Enregistrer la nouvelle liste des id_todo dans le fichier txt (ou le créer s'il n'existe pas encore)
            with open(id_todo_path, "r") as file:
                data = file.read()
            with open(id_todo_path, "w") as file:
                for post_id in id_todo:
                    file.write(post_id)

            # Ajouter le nb de commentaires traités dans le compteur
            updating_counter(counter_path, len(comments_data.index), current_post_id)

            # Fermer le fichier comment_manager
            comment_manager_file.close()
            
        else:
            # Retirer le premier id de la liste, le laisser à la fin, si le while est interrompu, il sera retiré alors que le post n'aura pas été traité
            id_todo.pop(0)

            # Enregistrer la nouvelle liste des id_todo dans le fichier txt (ou le créer s'il n'existe pas encore)
            with open(id_todo_path, "r") as file:
                data = file.read()
            with open(id_todo_path, "w") as file:
                for post_id in id_todo:
                    file.write(post_id)
                    
            # Fermer le fichier comment_manager
            comment_manager_file.close()
            
    else: # when list is empty
        print('')
        print('============================================')
        print('============================================')
        print('')
        print("La liste est vide, tout a été traité")

# Checker quels posts ont de nouveaux commentaires et les extraire
# id_todo est une liste des id a faire, et non le fichier.txt.
def check_new_comments_posts(id_todo):
    # ouvrir le csv, ou le créer
            
    # Check if file is empty (used to sed header or not)
    csv_exists = os.path.exists(csv_path.replace(os.sep, '/'))

    # Enregistrer au format csv avec pour nom la date
    dataframe.to_csv(csv_path, ';', mode='a', index=False, header= not csv_exists) 
    
    while id_todo:  # Vérifier si la liste n'est pas vide
        post.id = id_todo[0]
        id_todo.pop(0)

# Supprimer toute la data
def Delete_all_data():
    if os.path.isdir(subreddit_path):
        shutil.rmtree(subreddit_path)
        print('Dossier supprimé : ' + subreddit_path)
    else:
        print('Dossier inexistant : ' + subreddit_path)

#Delete_all_data()

def scrapping_main():
	###########################################
	
	# Traiter sub bitcoin
	
	# Récupérer le chemin du dossier contenant le script python
	script_folder = get_script_dir_path()
	# Créer un dossier pour le subreddit
	subreddit_path = create_folder(script_folder, subreddit_title)
	print(f'subreddit_path : {subreddit_path}')
	# Vérifier si le dossier comments (chemin relatif) existe, sinon le créer
	comments_path = create_folder(subreddit_path, 'comments')
	# Vérifier si le dossier comments_manager_id (chemin relatif) existe, sinon le créer
	comments_manager_id_path = create_folder(subreddit_path, 'comments_manager_id')
	# Créer la liste des id des posts à traiter
	id_todo_path = create_id_todo(subreddit_path)
	# Créer le fichier pour compter le nombre de commentaires total
	file_name = 'total_comments_counter.txt'
	counter_path = subreddit_path + file_name
	
	if not os.path.isfile(counter_path):
		counter_path = create_counter(subreddit_path)
	# Créer le compteur de commentaires par post, retourné par l'api (dans un fichier csv)
	print(f'SUBREDDIT PATH AVANT CREER CSV : {subreddit_path}')
	create_csv(subreddit_path, 'comments_manager_counter.csv')
	comments_manager_counter_path = subreddit_path + 'comments_manager_counter.csv'
	print('fonction 7')
	# Test if csv exists
	path_to_manager = 'C:\\Users\\Louis\\feelcrypt\\FeelCrypt\\scrapping_reddit\\scrapping_V5\\bitcoin\\comments_manager_counter.csv'
	counter_csv_exists = os.path.exists(path_to_manager.replace(os.sep, '/'))
	print("csv exists : " + str(counter_csv_exists))


	# Ouvrir la liste de posts pas encore faits
	with open(id_todo_path) as file:
		id_todo = file.readlines()

	# Traiter chaque id du fichier todo
	get_comments(id_todo, comments_manager_id_path, comments_manager_counter_path, id_todo_path, comments_path, counter_path, subreddit_path)
	
	############################################# 
	
	# Traiter sub btc
	
	# Récupérer le chemin du dossier contenant le script python
	script_folder = get_script_dir_path()
	# Créer un dossier pour le subreddit
	subreddit_path = create_folder(script_folder, subreddit_title2)
	print(f'subreddit_path : {subreddit_path}')
	# Vérifier si le dossier comments (chemin relatif) existe, sinon le créer
	comments_path = create_folder(subreddit_path, 'comments')
	# Vérifier si le dossier comments_manager_id (chemin relatif) existe, sinon le créer
	comments_manager_id_path = create_folder(subreddit_path, 'comments_manager_id')
	# Créer la liste des id des posts à traiter
	id_todo_path = create_id_todo(subreddit_path)
	# Créer le fichier pour compter le nombre de commentaires total
	file_name = 'total_comments_counter.txt'
	counter_path = subreddit_path + file_name
	
	if not os.path.isfile(counter_path):
		counter_path = create_counter(subreddit_path)
	# Créer le compteur de commentaires par post, retourné par l'api (dans un fichier csv)
	print(f'SUBREDDIT PATH AVANT CREER CSV : {subreddit_path}')
	create_csv(subreddit_path, 'comments_manager_counter.csv')
	comments_manager_counter_path = subreddit_path + 'comments_manager_counter.csv'
	print('fonction 7')
	# Test if csv exists
	path_to_manager = 'C:\\Users\\Louis\\feelcrypt\\FeelCrypt\\scrapping_reddit\\scrapping_V5\\btc\\comments_manager_counter.csv'
	counter_csv_exists = os.path.exists(path_to_manager.replace(os.sep, '/'))
	print("csv exists : " + str(counter_csv_exists))


	# Ouvrir la liste de posts pas encore faits
	with open(id_todo_path) as file:
		id_todo = file.readlines()

	# Traiter chaque id du fichier todo
	get_comments(id_todo, comments_manager_id_path, comments_manager_counter_path, id_todo_path, comments_path, counter_path, subreddit_path)
	
	
	