#!/usr/bin/env python

import pandas as pd
import numpy as np
import statsmodels.api as sm

from statsmodels.stats.outliers_influence import variance_inflation_factor
from patsy import dmatrices



df = pd.read_csv('ab_data.csv') # load data


######### Basic Info Check##############
# df.head() ## check the data
# df.nunique().user_id 
# df['converted'].describe()
# df.isna().sum()
########################################

# mismatch of old or new page and control or treatment group
# mark the mismatch data

df_treatment_old = df[(df['group'] == 'treatment') & (df['landing_page'] == 'old_page')]
df_control_new = df[(df['group'] == 'control') & (df['landing_page'] == 'new_page')]
mismatch = pd.concat([df_treatment_old, df_control_new])

# remove the mismatch data

df2 = df.drop(df_treatment_old.index)
df2 = df2.drop(df_control_new.index)

# check whether the duplicate data exists
df2[df2.user_id.duplicated()]

# remove the duplicates data
df2.drop_duplicates(subset = 'user_id', inplace = True)

# hypothesis test
old_convert = df2.query('landing_page == "old_page"').converted.sum()
new_convert = df2.query('landing_page == "new_page"').converted.sum()
old_number = df2.query('landing_page == "old_page"').user_id.count()
new_number = df2.query('landing_page == "new_page"').user_id.count()

count = np.array([new_convert, old_convert])
N = np.array([new_number, old_number])

z_score, p_val_z = sm.stats.proportions_ztest(count, N, alternative='larger')

if p_val_z > 0.05:
	print("Test fails based on hypothesis test")
else:
	print("Test succeeds based on hypothesis test")

## Logistic regression model can also be applied to this questions##

# generate new variables
df2['intercept'] = 1
df2[['ab_page', 'ab_drop']] = pd.get_dummies(df2['landing_page'])
df2.drop('ab_drop', axis = 1, inplace = True)

# train model
logistics_model = sm.Logit(df2['converted'], df2[['intercept', 'ab_page']])
train = logistics_model.fit()
print(train.summary())

# the P is larger than 0.05, so it proves the same result with hypothesis test

## Will it be related to the countries? #############################

df_country = pd.read_csv('countries.csv')
df3 = df2.merge(df_country, how = 'outer', on = 'user_id') # merge data

# generate variables
df3[['UK', 'US']] = pd.get_dummies(df3.country)

# train the model
logistics_model_with_country = sm.Logit(df3['converted'], df3[['intercept', 'ab_page', 'US', 'UK']])
tran_with_country = logistics_model_with_country.fit()
print(tran_with_country.summary())

# the P is larger than 0.05, so it proves no effect




