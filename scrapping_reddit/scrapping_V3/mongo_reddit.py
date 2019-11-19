# -*- coding: utf-8 -*-


# -- ==user_accounts== --
import pymongo
import json

with open('mongo_config.json') as json_data_file:
    config = json.load(json_data_file)

client = pymongo.MongoClient(f"mongodb+srv://{config['username']}:{config['password']}@cluster0-oebpl.mongodb.net/test?retryWrites=true&w=majority")
                             
mydb = client["RedditScraping"]
posts_collection = mydb["posts"]

def get_post_by_id(post_id):
    return posts_collection.find_one({"_id" : post_id})

def insert_post(post_id, title = "", url = "", comments_id = []):
    post = { "title": title, "url": url, "_id" : post_id, "comments_id" : comments_id }
    posts_collection.insert_one(post)
                             
def add_comments_id(post_id, comments_id):
    if isinstance(comments_id, list):
        for comment_id in comments_id:
            posts_collection.update_one({"_id" : post_id}, {"$push" : {"comments_id" : comment_id}})
    else: 
        posts_collection.update_one({"_id" : post_id}, {"$push" : {"comments_id" : comments_id}})                             

# -- ==user_accounts== --