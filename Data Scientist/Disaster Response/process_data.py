#!/usr/bin/env python

import sys
import pandas as pd
import numpy as np
import sqlite3
from sqlalchemy import create_engine

def load_data(messages_filepath, categories_filepath):
    # load data
    messages = pd.read_csv(messages_filepath)
    categories = pd.read_csv(categories_filepath)
    # merge messages and categories data
    df = messages.merge(categories, how = 'outer', on = ['id'])
    return df



def clean_data(df):
    # clean data in category column
    categories = df['categories'].str.split(";", expand = True)
    row = categories.iloc[1,]
    # split data in category column
    category_colnames = row.str.split("-").apply(lambda x: x[0])
    categories.columns = category_colnames
    
    # seperate category columns
    for column in categories:
        categories[column] = categories[column].str.split("-").apply(lambda x: x[1])
        categories[column] = categories[column].astype(int) # change type

    df.drop('categories', inplace = True, axis = 1)
    # combine into new dataframe
    df = pd.concat([df, categories], axis = 1)
    # drop duplicate data
    df = df.drop_duplicates()
    return df


def save_data(df, database_filename):
    engine = create_engine('sqlite:///' + database_filename)
    df.to_sql('InsertTableName', engine, index=False)


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()