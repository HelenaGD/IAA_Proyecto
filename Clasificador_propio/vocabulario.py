"""
Helena Garcia Diaz
26/04/2022

ref = https://spacy.io/usage/linguistic-features
ref = https://www.machinelearningplus.com/spacy-tutorial-nlp/
ref = https://stackoverflow.com/questions/57231616/valueerror-e088-text-of-length-1027203-exceeds-maximum-of-1000000-spacy
regular expresion for URLs = https://www.codegrepper.com/code-examples/python/regex+remove+URL
ref = https://stackoverflow.com/questions/17390326/getting-rid-of-stop-words-and-document-tokenization-using-nltk
types of tags for lemantization = https://stackoverflow.com/questions/29332851/what-does-nn-vbd-in-dt-nns-rb-means-in-nltk
"""

# Libraries
from typing import final
import spacy
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
#nltk.download('stopwords')
#nltk.download('punkt')
#nltk.download('wordnet')
#nltk.download('omw-1.4')
#nltk.download('averaged_perceptron_tagger')
import re
import string
import pandas as pd
from collections import OrderedDict

def nltk_pos_tagger(nltk_tag):
  etiqueta = nltk_tag[0][1]
  if etiqueta.startswith('J'):
    return wordnet.ADJ
  elif etiqueta.startswith('V'):
    return wordnet.VERB
  elif etiqueta.startswith('N'):
    return wordnet.NOUN
  elif etiqueta.startswith('R'):
    return wordnet.ADV
  else:          
    return None

# Load English tokenizer, tagger, parser and NER
stop = set(stopwords.words('english') + list(string.punctuation))
lemmantizer = WordNetLemmatizer()

data_tweets = pd.read_excel(r'COV_train.xlsx', index_col=None, engine='openpyxl', sheet_name='Sheet 1', usecols="A")
file = open("vocabulario.txt", "w")

raw_data = []
text = ""
amount_of_tweets = 0
for index, data in data_tweets.iterrows():
  # remove links
  reduced_text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ', data[0], flags=re.MULTILINE)
  # remove the numbers
  # ints
  reduced_text = re.sub(r'/^\d+\s|\s\d+\s|\s\d+$/', ' ', reduced_text, flags=re.MULTILINE)
  # floats with '.'
  reduced_text = re.sub(r'(\d*\.\d+)|(\d+\.[0-9 ]+)', ' ', reduced_text, flags=re.MULTILINE)
  # floats with ','
  reduced_text = re.sub(r'(\d*\,\d+)|(\d+\,[0-9 ]+)', ' ', reduced_text, flags=re.MULTILINE)
  # remove users
  reduced_text = re.sub(r'(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)', ' ', reduced_text, flags=re.MULTILINE)
  # remove hastahgs
  reduced_text = re.sub(r'(#[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)', ' ', reduced_text, flags=re.MULTILINE)
  # remove '...' with blank spaces
  reduced_text = re.sub(r'/.+', ' ', reduced_text, flags=re.MULTILINE)
  # remove line breakers
  reduced_text = ' '.join(reduced_text.splitlines())
  #remove multiple spaces
  reduced_text = ' '.join(reduced_text.split())
  text += reduced_text
  amount_of_tweets += 1
  if (amount_of_tweets > 3570):
    raw_data.append(text)
    amount_of_tweets = 0
    text = ""

#print(f'Length of the whole raw data {len(raw_data)}')
# Now I have the text divided
#for text in raw_data:
  #print(f'Length of the data: {len(text)}')

the_list_of_tokens = []
# Tokenization of each text
for text in raw_data:
  #doc = nlp(text)
  # Tokenice with nltk
  doc = [i for i in nltk.word_tokenize(text.lower()) if (i not in stop and not i.isdigit())]
  # Amount of tokens before
  #print(f'Amount of tokens before: {len(nlp(doc))}')
  #print(f'Amount of tokens before: {len(doc)}')

  # Remove stopwords, punctuations
  #doc = [token for token in doc if not token.is_stop and not token.is_punct]
  # Amount of tokens after
  #print(f'Amount of tokens after: {len(doc)}')
  for token in doc:
    token = re.sub(r'[0-9]', '', token)
    #the_list_of_tokens.append(token.text)
    the_list_of_tokens.append(token)

print(f'Len of other list of the tokens: {len(the_list_of_tokens)}')

# Order the list of tokens
the_list_of_tokens.sort()
# Left only one occurence
new_list = pd.unique(the_list_of_tokens).tolist()

final_list = []
# The lemantization
for word in new_list:
  nltk_tag = nltk_pos_tagger(nltk.tag.pos_tag([word]))
  final_list.append(lemmantizer.lemmatize(word))

final_list = pd.unique(final_list).tolist()
final_list.sort()

# Write on the file
file.write(f'Numero de palabras: {len(final_list)}\n')
for token in final_list:
  #print(token)
  file.write(f'{token}\n')

file.close()

