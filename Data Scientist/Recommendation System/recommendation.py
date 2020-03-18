#!/usr/bin/env python

import pandas as pd
import numpy as np



########################################Below is Rank-Based Recommendation################

def get_top_articles(n, df):
    '''
    INPUT:
    n - (int) the number of top articles to return
    df - (pandas dataframe) df as defined at the top of the notebook 
    
    OUTPUT:
    top_articles - (list) A list of the top 'n' article titles 
    
    '''
    
    return  df['title'].value_counts().index[:n].tolist() # Return the top article titles from df (not df_content)

def get_top_article_ids(n, df):
    '''
    INPUT:
    n - (int) the number of top articles to return
    df - (pandas dataframe) df as defined at the top of the notebook 
    
    OUTPUT:
    top_articles - (list) A list of the top 'n' article titles 
    
    '''
 
    return df['article_id'].value_counts().index[:n].tolist() # Return the top article ids



################################Below is User-User Based Collaborative Filtering############

# create the user-article matrix with 1's and 0's

def create_user_item_matrix(df):
    '''
    INPUT:
    df - pandas dataframe with article_id, title, user_id columns
    
    OUTPUT:
    user_item - user item matrix 
    
    Description:
    Return a matrix with user ids as rows and article ids on the columns with 1 values where a user interacted with 
    an article and a 0 otherwise
    '''

    user_item = df.groupby(['user_id', 'article_id'])['title'].count().notnull().unstack().notnull().astype(np.int)
    
    return user_item # return the user_item matrix 


def find_similar_users(user_id, user_item):
    '''
    INPUT:
    user_id - (int) a user_id
    user_item - (pandas dataframe) matrix of users by articles: 
                1's when a user has interacted with an article, 0 otherwise
    
    OUTPUT:
    similar_users - (list) an ordered list where the closest users (largest dot product users)
                    are listed first
    
    Description:
    Computes the similarity of every pair of users based on the dot product
    Returns an ordered
    
    '''
    # compute similarity of each user to the provided user
    similarity = user_item[user_item.index == user_id].dot(user_item.T)
    # sort by similarity
    sorted_similarity = similarity.sort_values(user_id, axis = 1, ascending = False)
  
    # create list of just the ids
    list_ids = sorted_similarity.columns.tolist()

    list_ids.remove(user_id) # remove the owner id


    return list_ids # return a list of the users in order from most to least similar


def get_article_names(article_ids, df):
    '''
    INPUT:
    article_ids - (list) a list of article ids
    df - (pandas dataframe) df as defined at the top of the notebook
    
    OUTPUT:
    article_names - (list) a list of article names associated with the list of article ids 
                    (this is identified by the title column)
    '''

    article_names = []
    for element in article_ids:
        article_names.extend(df[df['article_id'] == float(element)]['title'].drop_duplicates().tolist())
        
    return article_names # Return the article names associated with list of article ids


def get_user_articles(user_id, user_item, df):
    '''
    INPUT:
    user_id - (int) a user id
    user_item - (pandas dataframe) matrix of users by articles: 
                1's when a user has interacted with an article, 0 otherwise
    
    OUTPUT:
    article_ids - (list) a list of the article ids seen by the user
    article_names - (list) a list of article names associated with the list of article ids 
                    (this is identified by the doc_full_name column in df_content)
    
    Description:
    Provides a list of the article_ids and article titles that have been seen by a user
    '''

    article_ids = user_item.loc[user_id].where(user_item.loc[user_id] == 1).dropna().index.tolist()
   
    article_names = get_article_names(article_ids, df)
    
    return article_ids, article_names # return the ids and names


def user_user_recs(user_id, user_item, df, m=10):
    '''
    INPUT:
    user_id - (int) a user id
    m - (int) the number of recommendations you want for the user
    
    OUTPUT:
    recs - (list) a list of recommendations for the user
    
    Description:
    Loops through the users based on closeness to the input user_id
    For each user - finds articles the user hasn't seen before and provides them as recs
    Does this until m recommendations are found
    
    Notes:
    Users who are the same closeness are chosen arbitrarily as the 'next' user
    
    For the user where the number of recommended articles starts below m 
    and ends exceeding m, the last items are chosen arbitrarily
    
    '''

    recs = []
    similarity_user = find_similar_users(user_id, user_item)
    user_seen_article_id, user_seen_article_name = get_user_articles(user_id, user_item, df) # get the info of owner
    
    for user in similarity_user:
        similarity_article_id, similarity_article_name = get_user_articles(user, user_item, df) # get the info of similarity user
        article_not_seen = np.setdiff1d(np.array(similarity_article_id), 
        								np.array(user_seen_article_id), assume_unique = True).tolist() # not seen by owner
        recs.extend(article_not_seen)
        recs = pd.Series(recs).drop_duplicates().tolist()
        
        
        if len(recs) >= m: # m is the maximum value for number of recommendations
            break
    
    recs = recs[:m]

    return recs # return your recommendations for this user_id    

####################################################################################

def email_mapper(df):
    coded_dict = dict()
    cter = 1
    email_encoded = []
    
    for val in df['email']:
        if val not in coded_dict:
            coded_dict[val] = cter
            cter+=1
        
        email_encoded.append(coded_dict[val])

    return email_encoded


def main():

	# pre-process data
	df = pd.read_csv('user-item-interactions.csv') # data is not provided here
	del df['Unnamed: 0']
	
	# exchange email column with user_id
	email_encoded = email_mapper(df)
	del df['email']
	df['user_id'] = email_encoded

	# Below runs for Rank-Based Recommendation
	print(get_top_articles(10, df))  #### This can give you a result based on article titles
	print(get_top_article_ids(10, df))  #### This can give you a result based on article ids

	# Below runs for User-User Based Recommendation
	user_item = create_user_item_matrix(df) 

	article_name = get_article_names(user_user_recs(1, user_item, df, 10), df) # Return 10 recommendations for user 1

	print(article_name)


main() # run the code








