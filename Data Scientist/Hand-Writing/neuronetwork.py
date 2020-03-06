#!/usr/bin/env python
# coding: utf-8

import numpy as np
import torch
import pandas as pd
import torch.nn.functional as F
from torch import nn, optim



class NeuroNetwork(nn.Module):
	def __init__(self):
		super().__init__()
		self.fc1 = nn.Linear(784, 300)
		self.fc2 = nn.Linear(300, 200)
		self.fc3 = nn.Linear(200, 100)
		self.fc4 = nn.Linear(100, 10)
        
		self.dropout = nn.Dropout(p = 0.2) # in case of overfitting
        
	def forward(self, x):
        
		x = x.view(x.shape[0], -1) # flatten tensor
        
		# calculation funcation with dropout
		x = self.dropout(F.relu(self.fc1(x)))
		x = self.dropout(F.relu(self.fc2(x)))
		x = self.dropout(F.relu(self.fc3(x)))
		x = F.log_softmax(self.fc4(x), dim=1)
		
		return x

