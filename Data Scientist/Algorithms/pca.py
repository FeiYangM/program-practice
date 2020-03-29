#!/usr/bin/env python

import numpy as np
import pandas as pd
import sys

'''
Usage: python pca.py input.csv
      
       input.csv: row is different sample, and column is features of them. This program reads 
                  from second line of this input csv file
       output will be printed on screen
'''



class PCA_algorithm:
	def __init__(self, data):
		self.datasets = data

	def zeroMeans(self):
		# calculate the matrix minus the mean
		mean_array = np.mean(self.datasets, axis = 0)
		new_data = self.datasets - mean_array

		return new_data, mean_array

	def covariance(self, post_data):
		# calculate co-variance
		cov_matrix = np.cov(post_data, rowvar=0)

		return cov_matrix

	def Eigenvalue(self, cov_data):
		# calculate Eigen info
		eigValue, eigVector = np.linalg.eig(np.mat(cov_data))

		return  eigValue, eigVector

	def k_choose(self, eigvalue, percentage = 0.99):
		# basically use the 99% variance to determine the value of k
		sort_array = np.sort(eigvalue)
		sort_array = sort_array[-1::-1]
		sum_array = sum(sort_array)
		total = 0
		number = 0
		for i in sort_array:
			total += 1
			number += 1
			if total >= sum_array * percentage:
				return number

def main(filename):
	# read data file
	input_data = pd.read_csv(filename)
	input_array = np.array(input_data)

	# call class model
	model = PCA_algorithm(input_array)
	new_data, mean_matrix = model.zeroMeans()
	cov_matrix = model.covariance(new_data)
	eigValue, eigVector = model.Eigenvalue(cov_matrix)
	n = model.k_choose(eigValue, 0.99) # n is k

	# transform data
	eigNew = np.argsort(eigValue)
	n_eigNew = eigNew[-1:-(n+1):-1]
	new_array = eigVector[:, n_eigNew]

	# generate lower dimensional data
	lower_data = new_data * new_array
	# the constructed data: sometimes it makes analysis simple
	construct_data = (lower_data * new_array.T) + mean_matrix 
	return lower_data, construct_data


if __name__ == '__main__':
	filename = sys.argv[1]
	# run the program
	low_dimension, reconstruct_data = main(filename)
	print("reconstucted data is:")
	print(reconstruct_data)
	print("\n\n\n")
	print("lower dimensional data is:")
	print(low_dimension)







