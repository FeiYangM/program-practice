#!/usr/bin/env python
# coding: utf-8

import sys,os, getopt
import numpy as np
import torch
import matplotlib.pyplot as plt
import pandas as pd

from neuronetwork import *
from torchvision import datasets, transforms
from torch import nn, optim

def prepare_data(folder_data):
	transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,),(0.5,))])

	# download train and test datasets to the provided folder
	train_data = datasets.MNIST(folder_data, download = True, train = True, transform = transform)
	test_data = datasets.MNIST(folder_data, download = True, train = False, transform = transform)
	
	# split the train data into train and validation datasets
	train_data, val_data = torch.utils.data.dataset.random_split(train_data, [50000, 10000])
	print('train:', len(train_data), 'test:', len(test_data), 'val:', len(val_data))

	# load data
	train_data_loader = torch.utils.data.DataLoader(train_data, batch_size = 64, shuffle = True)
	val_data_loader = torch.utils.data.DataLoader(val_data, batch_size = 64, shuffle = True)
	test_data_loader = torch.utils.data.DataLoader(test_data, batch_size = 64, shuffle = True)

	return train_data_loader, val_data_loader, test_data_loader

def train_nnmodel(folder_data, epochs, learnrate):
	
	train_data_loader, val_data_loader, test_data_loader = prepare_data(folder_data) # prepare data

	#build model and initial defined
	handwriting_model = NeuroNetwork()
	criterion = nn.CrossEntropyLoss()
	optimizer = optim.Adam(handwriting_model.parameters(), lr = learnrate)
	
	train_loss, val_loss, test_loss = [], [], []

	for step in range(epochs):
		running_loss = 0
		for images, labels in train_data_loader:
			optimizer.zero_grad() # remove the accumulated gradient from last step
        
			score = handwriting_model(images)
			loss = criterion(score, labels)
			loss.backward()
			optimizer.step()
			running_loss += loss.item()
        
		val_losses = 0   
		accuracy = 0
		with torch.no_grad(): # close backward for the validation step
			handwriting_model.eval() # close dropout because this step is used for validation
			
			for val_images, val_labels in val_data_loader:
				val_score = handwriting_model(val_images)
				val_losses += criterion(val_score, val_labels).item()
				prob = torch.exp(val_score)
				top_p, top_class = prob.topk(1, dim = 1)
				equals = top_class == val_labels.view(*top_class.shape) # compare label and calculated result
				accuracy += torch.mean(equals.type(torch.FloatTensor))
		
		train_loss.append(running_loss/len(train_data_loader))
		val_loss.append(val_losses/len(val_data_loader))
		print("Epoch:{}/{}".format(step+1, epochs),
		      "train_loss:{:.3f}".format(running_loss/len(train_data_loader)),
		      "val_loss:{:.3f}".format(val_losses/len(val_data_loader)),
		      "accuracy:{:.3f}".format(accuracy/len(val_data_loader)))

	plt.plot(train_loss, label='Training loss')
	plt.plot(val_loss, label='Validation loss')
	plt.legend(frameon=False)


def do(args):
	usage = """
			python main.py [option]
			
			options:
			-f: /abs_path/to/data_folder to download MNIST data 
			-e: number for iter
			-l: learnrate 

			ex: python main.py -f abs_folder -e 30 -l 0.03
			"""
	opts, arg = getopt.getopt(args, "hf:e:l:")
	data_folder = ""
	epochs = ""
	learnrate = ""
	count = 0
	for op, value in opts:
		if op == "-f":
			data_folder = value
		elif op == "-e":
			epochs = int(value)
		elif op == "-l":
			learnrate = float(value)
		elif op == "-h":
			count += 1
			print(usage)
			sys.exit()
	if count == 0 and len(sys.argv) < 7:
		print("\n")
		print("\t\tNo enough parameters.Please see usage printed out",end="\n")
		print(usage)
		sys.exit()
	train_nnmodel(data_folder, epochs, learnrate)



if __name__ == '__main__':
	do(sys.argv[1:])






