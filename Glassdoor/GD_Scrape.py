from pymongo import MongoClient
import datetime
import reviews_data
# from nltk.tokenize import sent_tokenize, word_tokenize
# from nltk.corpus import stopwords
# import re
# import string
# from gensim import corpora, models, similarities
import matplotlib.pyplot as plt
import utils
import numpy as np

# DB settings
client = MongoClient()
indeed_db = client.indeed
indeed_jobs = indeed_db.jobs
indeed_reviews = indeed_db.reviews
glassdoor_db = client.glassdoor
glassdoor_reviews = glassdoor_db.reviews

companies = list(set(utils.get_company_names(indeed_reviews)))
ratings = reviews_data.all_ratings(indeed_reviews, glassdoor_reviews)

kept_ratings = []
# Drop ratings without any rating information
for rating in ratings:
    if len(rating) > 1:
        kept_ratings.append(rating)
ratings = kept_ratings
len(ratings)

ratings[0]

# returns the ratings for a company
# Possible keys: 'Comp & Benefits', 'Culture & Values','Career Opportunities',
# 'Senior Management', 'Work/Life Balance', and 'rating'
def get_company_ratings(company, ratings, key):
    company_ratings = []
    for rating in ratings:
        if rating['company'].lower() == company.lower() and key in rating:
            company_ratings.append(float(rating[key]))
    return company_ratings

# Plot ratings histograms
def draw_scores(scores, title="", show = True, save = False):
    if len(scores) == 0:
        print "No scores to plot"
        return
    hist = np.histogram(scores,bins=5,range=[0.01,5.01])[0] # for rounding
    draw_hist(hist, title, show, save)

def draw_hist(hist, title = "", show = True, save = False):
    plt.figure(figsize=(8,6))
    plt.bar([x+0.6 for x in range(5)], hist)
    plt.title(title,fontsize=25)
    plt.xlabel("Stars",fontsize=16)
    plt.ylabel("Number of reviews",fontsize=16)
    plt.xticks([0,1,2,3,4,5])
    plt.tick_params(labelsize=12)
    if save:
        plt.savefig('images/' + title.replace('/','-').replace(' ','_') + ".png")
    if show: plt.show()
    plt.close()
    return

def draw_all_company_rating(rating_key, companies_list, title_end):
    for company in companies_list:
        scores = get_company_ratings(company, ratings, rating_key)
        title = company + title_end
        draw_scores(scores, title, False, True);