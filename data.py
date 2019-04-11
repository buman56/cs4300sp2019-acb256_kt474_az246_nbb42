from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas
import math

df = pandas.read_csv('tripadvisor_merged.csv')
desc = []
for d in df["Description"]:
	
	if isinstance(d,float) and (math.isnan(d)):
		desc.append("")
	else:
		desc.append(d)
		
vectorizer = TfidfVectorizer(stop_words = 'english', max_df = .8,min_df = 10)
my_matrix = vectorizer.fit_transform(desc)
print(type(my_matrix))
print(my_matrix.shape)