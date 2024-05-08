import json
import requests
from elasticsearch import Elasticsearch
import tqdm.auto import tqdm



def download_data_json():

    filename = DATA_URL.split("/")[-1]

    if os.path.exists(filename):
        print(f"{filename}" already exists!)
    else:
        response = requests.get(DATA_URL)
        if response.status_code == 200:
            with open("document.json", "wb") as file:
                file.write(response.content)
                print("File downloaded successfully!")
        else:
            print(f"Failed to download the file. Errorcode: {response.status_code}")


def prepare_document(filename: str ='./documents.json'):
    """
    documents preprocessing
    """
    with open(filename, 'rt') as f_in:
        documents_file = json.load(f_in)

    documents = []

    for course in documents_file:
        course_name = course['course']

        for doc in course['documents']:
            doc['course'] = course_name
            documents.append(doc)

    return documents


def check_es_connection():
    es = Elasticsearch(ES_HOST)
    print (f"Elastic search runing with the following information:\n{es.info()}")
    
    

def generate_indexes(index_name="course-questions"):
    es = Elasticsearch(ES_HOST)
    index_settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "text": {"type": "text"},
                "section": {"type": "text"},
                "question": {"type": "text"},
                "course": {"type": "keyword"} 
            }
        }
    }

    response = es.indices.create(index=index_name, body=index_settings)

    for doc in tqdm(documents):
    es.index(index=index_name, document=doc)

    return es


def retrieve_documents(query, index_name="course-questions", top_n=5):
    es = Elasticsearch(ES_HOST)
    
    search_query = {
        "size": top_n,
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": query,
                        "fields": ["question^3", "text", "section"],
                        "type": "best_fields"
                    }
                },
                "filter": {
                    "term": {
                        "course": "data-engineering-zoomcamp"
                    }
                }
            }
        }
    }
    
    response = es.search(index=index_name, body=search_query)
    documents = [hit['_source'] for hit in response['hits']['hits']]

    return documents