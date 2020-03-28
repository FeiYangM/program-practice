#!/usr/bin/env python

import numpy as np
import pandas as pd
import random
import sys

class k_means_al:
	def __init__(self, datasets1, k):
		self.data = datasets1
		self.classN = k

	def random_center(self): 
		# initial matrix for centroid
		center = np.zeros((self.classN, self.data.shape[1]))
		for i in range(self.data.shape[1]):
			dmin, dmax = np.min(self.data[:,i]), np.max(self.data[:,i])
			center[:,i] = dmin + (dmax - dmin) * np.random.rand(self.classN)
		return center

	def dis_calcu(self, point1, point2):
		# calculate the distance between samples and centroids
		return np.sqrt(np.sum((point1 - point2) ** 2))

	def converged(self, old_center, new_center):
		# determine whether converged
		return (set([tuple(a) for a in old_center]) == set([tuple(b) for b in new_center]))

def classifier(data, k):
	# initial parameters
	datasets_arr = data
	label = np.zeros(datasets_arr.shape[0], dtype = np.int)
	cost = np.zeros(datasets_arr.shape[0])

	# use class model
	model = k_means_al(datasets_arr, k)
	center = model.random_center()

	converg = False

	while not converg:
		old_center = np.copy(center)

		# iterable
		for i in range(datasets_arr.shape[0]):
			min_dist = np.inf

			for j in range(k):
				dist = model.dis_calcu(datasets_arr[i], center[j])
				if dist < min_dist:
					min_dist = dist
					label[i] = j
			cost[i] =  model.dis_calcu(datasets_arr[i], center[label[i]]) ** 2
		# calculate the centroids
		for m in range(k):
			center[m] =  np.mean(datasets_arr[label == m], axis = 0)

		converg = model.converged(old_center, center)
	return center, label, np.sum(cost)


def main(filename, k):
	# initial parameters
	datasets1 = pd.read_csv(filename)
	datasets_arr1 = np.array(datasets1)
	# initial parameters
	lowest_cost = np.inf
	best_center = None
	best_label = None

	# iterable steps
	for i in range(10):
		centers, labels, costs = classifier(datasets_arr1, k)
		if costs < lowest_cost:
			lowest_cost = costs
			best_center = centers
			best_label = labels
	
	print(best_label) # the result for class



if __name__ == '__main__':
	filename = sys.argv[1]
	N = int(sys.argv[2])
	main(filename, N)




