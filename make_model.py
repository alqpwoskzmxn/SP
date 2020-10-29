import json
import re

from konlpy.tag import Okt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
import joblib

directory = './'
filename = 'parsed'

okt = Okt()

with open(directory + filename + '.json', 'r', encoding="UTF-8") as jsonfile:
  trainjson = json.load(jsonfile)

tag = list()
train_list = list()

for category in trainjson:
    for document in trainjson[category]:
        tag.append(category)
        temp = okt.morphs(document, stem=True)
        train_list.append(' '.join(temp))

tfidfvect = TfidfVectorizer()
tfidfvect.fit_transform(train_list)

train_tf_idf = tfidfvect.transform(train_list).toarray().tolist()

classifier = LinearSVC(C=0.8, max_iter=1000)
classifier.fit(train_tf_idf, tag)

joblib.dump(classifier, 'model.pkl')
joblib.dump(tfidfvect, 'tfidf.pkl')
