import time 
from flask import Flask
from markupsafe import escape

from pickle import TRUE
from pydoc import resolve
import requests
import sparqldataframe
import pandas as pd
import os 
from pydoc_data.topics import topics
import requests
import os
import pandas as pd
# Usual imports
import numpy as np
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt
from sklearn.decomposition import NMF, LatentDirichletAllocation, TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.manifold import TSNE
#import pyLDAvis.sklearn
from pylab import bone, pcolor, colorbar, plot, show, rcParams, savefig
import warnings
warnings.filterwarnings('ignore')
# Plotly based imports for visualization
# from plotly import tools
# import plotly.plotly as py
# from plotly.offline import init_notebook_mode, iplot
# import plotly.graph_objs as go
# import plotly.figure_factory as ff
# spaCy based imports
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.lang.en import English
import string
from time import time
import matplotlib.pyplot as plt
import json
from flask_cors import CORS

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation


os.chdir(os.path.dirname(os.path.abspath(__file__)))
pd.set_option("display.max_rows", None, "display.max_columns", None)
pd.set_option('display.max_colwidth', None)

nlp = spacy.load('en_core_web_sm')

punctuations = string.punctuation
stopwords = list(STOP_WORDS)

app = Flask(__name__)
CORS (app)

@app.route ('/time/<query>')
def wikiquery (query):
    
    query= query.strip()
    query = query.replace(' ', "%20")
    print(query)

    response = requests.get("https://www.wikidata.org/w/api.php?action=wbsearchentities&format=json&errorformat=plaintext&language=en&uselang=en&type=item&search="+ query)
    response = response.json()
    response = response ["search"][0]["id"]
    print(response)
    sparql_query ='''
    SELECT ?propUrl ?propLabel ?valUrl ?valLabel WHERE {
    
    wd:''' + response + '''
    ?propUrl ?valUrl.
    ?property ?ref ?propUrl;
    rdf:type wikibase:Property;
    rdfs:label ?propLabel.
    ?valUrl rdfs:label ?valLabel.
    FILTER((LANG(?valLabel)) = "en")
    FILTER((LANG(?propLabel)) = "en")
    }
    ORDER BY (?propUrl) (?valUrl)
    ''' 
    df = sparqldataframe.query("https://query.wikidata.org/sparql", sparql_query)

    df_source = df.drop(["propUrl", "valUrl", "valLabel"], axis=1)
    df_source = df_source.drop_duplicates(subset=['propLabel'])
    df_source["level"] = 2
    df_source["group"] = 1
    df_source["size"] = 15
    df_source = df_source.rename (columns={'propLabel': "name"})
    df_source = df_source[["name", "group", "size", "level"]]
    #print(df_source)

    df_source_1 = df_source.drop(["group", "size", "level"], axis=1)
    df_source_1 = df_source_1.rename(columns={"name":"target"})
    df_source_1["source"] = 1
    df_source_1["targetNode"]= df_source_1["target"]
    df_source_1 = df_source_1[["source", "target", "targetNode"]]
    #print(df_source_1)

    df_source_2 = df.drop(["propUrl", "propLabel", "valUrl"], axis=1)
    df_source_2["level"] = 3
    df_source_2["group"] = 2
    df_source_2["size"] = 35
    df_source_2 = df_source_2.rename(columns={"valLabel": "name"})
    df_source_2 = df_source_2[["name", "group", "size", "level"]]
    #print(df_source_2)

    df_source_3 = df.drop(["propUrl", "valUrl"], axis=1)
    df_source_3 = df_source_3.rename(columns={"propLabel":"source", "valLabel":"target"})
    df_source_3["targetNode"] = df_source_3["target"]
    df_source_3 = df_source_3[["source", "target", "targetNode"]]

    #print(df_source_3)

    df_source_4 = pd.DataFrame({"name": [1], "group": [4], "size": [50], "level": [0]})

    #print(df_source_4)
    

    semantic = requests.get(f"https://api.semanticscholar.org/graph/v1/paper/search?query={query}&fields=abstract&limit=100")

    semantic = semantic.json()
    df = semantic["data"]

    semantic = pd.DataFrame(df)
    df = semantic["abstract"].tolist()

    df =  [x for x in df if x != None]

    n_samples = 2000
    n_features = 1000
    n_components = 10
    n_top_words = 5

    data_samples = df

    tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, max_features=n_features, stop_words="english")

    tfidf = tfidf_vectorizer.fit_transform(data_samples)


    #print(df)
    nmf = NMF(n_components=n_components, random_state=1, alpha=0.1, l1_ratio=0.5).fit(tfidf)


    tfidf_feature_names = tfidf_vectorizer.get_feature_names_out()


    a = []
    b = []

    for topic_idx, topic in enumerate(nmf.components_):
        top_features_ind = topic.argsort()[: -n_top_words - 1 : -1]
        top_features = [tfidf_feature_names[i] for i in top_features_ind]
        a.append(top_features)
        weights = topic[top_features_ind]
        b.append(weights)


    a = np.array(a)
    a = a.flatten()
    b = np.array(b)
    b = b.flatten()

    c = []

    for elem in zip(a, b):
        c.extend(elem)

    c = np.array(c)
    c = np.split(c, 50)
    index_retrieve=["topic"+str(x//5) for x in range((50)*1)]


    f = pd.DataFrame(c, columns = ['name','size'])
    f ["topic"] = index_retrieve
    f ["level"] = -2
    f ["group"] = 3
    f["size" ] = 2
    f = f.drop_duplicates(subset=['name'])
    topic_nodes = f.drop (["topic"], axis=1)
    topic_nodes = topic_nodes [["name", "group", "size", "level"]]

    #print(topic_nodes)
    
    topic_nodes_1 = ({"name": ["topic0", "topic1", "topic2", "topic3", "topic4", "topic5", "topic6", "topic7", "topic8", "topic9"]})
    topic_nodes_1["group"] = 4
    topic_nodes_1["size"] = 15
    topic_nodes_1["level"] = -1
    topic_nodes_1 = pd.DataFrame (topic_nodes_1)

    #print(topic_nodes_1)

    link_topic_nodes_1 = topic_nodes_1.drop(["group", "size", "level"], axis =1)
    link_topic_nodes_1["source"] = 1
    link_topic_nodes_1  = link_topic_nodes_1.rename (columns={"name":"target"})
    link_topic_nodes_1["targetNode"] = link_topic_nodes_1["target"]
    link_topic_nodes_1 = link_topic_nodes_1[["source", "target", "targetNode"]]

    #print(link_topic_nodes_1)

    link_topic_nodes_2 = f.drop(["level", "group", "size"], axis =1)
    link_topic_nodes_2= link_topic_nodes_2.rename(columns={"name":"target", "topic":"source"})
    link_topic_nodes_2["targetNode"] = link_topic_nodes_2["target"]
    link_topic_nodes_2 = link_topic_nodes_2[["source", "target", "targetNode"]]

    #print(link_topic_nodes_2)
    node_pandas_1 = df_source.to_dict("records")
    link_pandas_1 = df_source_1.to_dict("records")
    node_pandas_2 = df_source_2.to_dict("records")
    link_pandas_2 = df_source_3.to_dict('records')
    node_pandas_3 = df_source_4.to_dict("records")
    topic_nodes = topic_nodes.to_dict("records")
    topic_nodes_1 = topic_nodes_1.to_dict("records")
    link_topic_nodes_1 = link_topic_nodes_1.to_dict("records")
    link_topic_nodes_2=link_topic_nodes_2.to_dict("records")


    nodes = node_pandas_1 + node_pandas_2 + node_pandas_3 + topic_nodes + topic_nodes_1
    links = link_pandas_1 + link_pandas_2 + link_topic_nodes_1 + link_topic_nodes_2

    #print(nodes)


    final = {"nodes": nodes, "links": links}

    #print(final)
    return final 

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(final, f, ensure_ascii=False, indent=4)   

if __name__=='__main__':
    app.run(host="0.0.0.0", threaded= True, port=5000)
