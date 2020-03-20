#!/usr/bin/env python

import pandas as pd
import numpy as np
import sqlite3
import nltk
import re
import pickle
import sys

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sqlalchemy import create_engine
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV

def load_data(database_filepath):
	# load data from sql database
	engine = create_engine('sqlite:///' + database_filepath)
	df = pd.read_sql_table('InsertTableName', engine)
	# pre-process data
	df.related.replace(2, 1, inplace=True)
	X = df['message'] 
	Y = df.loc[:, 'related' : 'direct_report']
	target_names = df.loc[:,'related':'direct_report'].columns.tolist()

	return X, Y, target_names


def tokenize(text):
	# pre-process data
	text = re.sub(r'[^a-zA-Z0-9]', " ", text.lower())
	# token words	
	token = word_tokenize(text)
	# initiate lemmatizer
	lemmatizer = WordNetLemmatizer()

	clean_token = []
	for tok in token:
		clean_tok = lemmatizer.lemmatize(tok).strip()
		clean_token.append(clean_tok)

	return clean_token


def build_model():
	# create a pipeline
	pipeline = Pipeline([('vect', CountVectorizer(tokenizer = tokenize)),
			     ('tfidf', TfidfTransformer()),
			     ('clf', MultiOutputClassifier(RandomForestClassifier()))])

	return pipeline



def evaluate_model(model, X_test, Y_test, category_names):
	# evaluate model
	Y_predict = model.predict(X_test)
	Y_predict = pd.DataFrame(Y_predict, columns = category_names)
	for col in range(36):
		print(target_names[col], "\n", classification_report(Y_test.iloc[:,col], Y_predict.iloc[:,col]))

	


def save_model(model, model_filepath):
	pickle.dump(model, open(model_filepath, 'wb'))


def main():
	if len(sys.argv) == 3:
		database_filepath, model_filepath = sys.argv[1:]
		print('Loading data...\n    DATABASE: {}'.format(database_filepath))
		X, Y, category_names = load_data(database_filepath)
		X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

        	print('Building model...')
        	model = build_model()

		print('Training model...')
		model.fit(X_train, Y_train)

		print('Evaluating model...')
		evaluate_model(model, X_test, Y_test, category_names)

		print('Saving model...\n    MODEL: {}'.format(model_filepath))
		save_model(model, model_filepath)

		print('Trained model saved!')

	else:
		print('Please provide the filepath of the disaster messages database '\
			'as the first argument and the filepath of the pickle file to '\
			'save the model to as the second argument. \n\nExample: python '\
			'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()
