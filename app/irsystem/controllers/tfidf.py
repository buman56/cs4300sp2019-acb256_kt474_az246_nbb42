import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import math
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse.linalg import svds
from sklearn.preprocessing import normalize
import json

df = pd.read_csv('tripadvisor_merged.csv')
with open('review_quote_world.json') as json_file:
    review_js = json.load(json_file)
review_museum = (review_js.keys())

desc_data = []
for d in df['Description']:
    if (isinstance(d, float)):
        if (math.isnan(d)):
            desc_data.append('')
    else:
        desc_data.append(d)
pure_desc = desc_data.copy()

m_index_to_name = {
    index: m_name
    for index, m_name in enumerate(df['MuseumName'])
}

m_index_to_address = {
    index: m_name
    for index, m_name in enumerate(df['Address'])
}

m_index_to_lat = {index: m_name for index, m_name in enumerate(df['Latitude'])}
m_index_to_lng = {
    index: m_name
    for index, m_name in enumerate(df['Langtitude'])
}
m_name_to_index = dict((v, k) for k, v in m_index_to_name.items())

for m in review_museum:
    ind = m_name_to_index[m]
    for review in review_js[m]:
        desc_data[ind] = desc_data[ind] + review

m_index_to_description = {index: desc for index, desc in enumerate(pure_desc)}

# image stuff
link = "https://source.unsplash.com/1600x900/?"


def build_vectorizer(max_features, stop_words, max_df=0.8, min_df=1,
                     norm='l2'):
    return TfidfVectorizer(stop_words=stop_words,
                           max_df=max_df,
                           min_df=min_df,
                           max_features=max_features,
                           norm=norm)


def get_sim(query, doc_index, doc_by_vocab):
    return cosine_similarity(query, doc_by_vocab)


def closest_projects(docs_compressed, project_index_in, k=5):
    sims = docs_compressed.dot(docs_compressed[project_index_in, :])
    asort = np.argsort(-sims)[:k + 1]
    # return [(m_index_to_name[i], sims[i] / sims[asort[0]],
    #          m_index_to_description[i]) for i in asort[1:]]
    #changed so it only returns the title for now
    return [(m_index_to_name[i]) for i in asort[1:]]


def museum_match(q):

    vectorizer = build_vectorizer(5000, "english")
    doc_by_vocab = vectorizer.fit_transform(desc_data).transpose()

    words_compressed, _, docs_compressed = svds(doc_by_vocab, k=40)
    docs_compressed = docs_compressed.transpose()

    docs_compressed = normalize(docs_compressed, axis=1)

    return closest_projects(docs_compressed, m_name_to_index[q], 5)


def get_suggestions(q):
    vectorizer = build_vectorizer(5000, "english")
    doc_by_vocab = vectorizer.fit_transform(desc_data)
    query = vectorizer.transform([q])
    sim = get_sim(query, 5, doc_by_vocab)[0]
    top_5_idx = np.argsort(sim)[-5:]
    top_5 = []

    for i in reversed(top_5_idx):
        if (sim[i] > 0 and m_index_to_description[i] != ''):
            keyword = m_index_to_name[i].split()
            top_5.append(
                (m_index_to_name[i], sim[i],
                 m_index_to_description[i], link + 'museum,' + keyword[0],
                 museum_match(m_index_to_name[i]), m_index_to_address[i],
                 m_index_to_lat[i], m_index_to_lng[i]))

    return top_5


def OLD_get_suggestions(q):
    df = pd.read_csv('tripadvisor_merged.csv')
    desc_data = []
    #
    for d in df['Description']:
        if (isinstance(d, float)):
            if (math.isnan(d)):
                desc_data.append('')
        else:
            desc_data.append(d)

    movie_index_to_name = {
        index: movie_name
        for index, movie_name in enumerate(df['MuseumName'])
    }
    movie_index_to_description = {
        index: desc
        for index, desc in enumerate(desc_data)
    }

    vectorizer = build_vectorizer(5000, "english")
    doc_by_vocab = vectorizer.fit_transform(desc_data)
    query = vectorizer.transform([q])
    sim = get_sim(query, 5, doc_by_vocab)[0]
    top_5_idx = np.argsort(sim)[-5:]
    top_5 = []

    for i in reversed(top_5_idx):
        top_5.append(
            (movie_index_to_name[i], sim[i], movie_index_to_description[i]))

    return top_5


def main():
    print(get_suggestions('war memorial service'))
    print(museum_match("he"))


if __name__ == "__main__":
    main()
