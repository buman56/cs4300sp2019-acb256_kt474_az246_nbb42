import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import math
from sklearn.metrics.pairwise import cosine_similarity


def build_vectorizer(max_features, stop_words, max_df=0.8, min_df=1,
                     norm='l2'):
    return TfidfVectorizer(stop_words=stop_words,
                           max_df=max_df,
                           min_df=min_df,
                           max_features=max_features,
                           norm=norm)


def get_sim(query, doc_index, doc_by_vocab):
    return cosine_similarity(query, doc_by_vocab)


def get_suggestions(q):
    df = pd.read_csv('tripadvisor_merged.csv')
    desc_data = []

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


if __name__ == "__main__":
    main()
