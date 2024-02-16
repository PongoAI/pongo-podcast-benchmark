from datasets import load_dataset
from llama_index import VectorStoreIndex
from llama_index.vector_stores import PineconeVectorStore
import pinecone
from llama_index.embeddings import HuggingFaceEmbedding
import csv
from openai import OpenAI
import openai
from llama_index.node_parser import SentenceSplitter
from llama_index import ServiceContext
from llama_index.embeddings import OpenAIEmbedding
import time


embed_model = OpenAIEmbedding(model="text-embedding-3-large", api_key='YOUR_OPENAI_KEY', dimensions=3072)

pinecone_api_key = 'YOUR_PINECONE_KEY'
pinecone_environment = 'us-east1-gcp'
pinecone.init(api_key=pinecone_api_key, environment=pinecone_environment)

index_name = 'oai-large-podcast'

pinecone_index = pinecone.Index(index_name)

vector_store = PineconeVectorStore(pinecone_index=pinecone_index)

# storage_context = StorageContext.from_defaults(vector_store = vector_store)
text_splitter = SentenceSplitter(
        chunk_size=1024,
        separator=" ",
        chunk_overlap=128
    )
service_context = ServiceContext.from_defaults(llm=None, embed_model=embed_model, text_splitter=text_splitter)

index = VectorStoreIndex.from_vector_store(vector_store, service_context=service_context)    

retriever = index.as_retriever(similarity_top_k=10)

file_exists = False
try:
    with open('../results/llamaindex-benchmark-results.csv', 'r') as file:
        file_exists = True
except FileNotFoundError:
    pass

if not file_exists:
    with open('../results/llamaindex-benchmark-results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["question", 'answer', 'context'])

vectorized_questions = []
starting_datapoint_index = 0
datapoint_index = starting_datapoint_index #long-running task so enable stopping and starting partway through

# try:
with open('../results/llamaindex-benchmark-results.csv', 'a', newline='') as file, \
        open('../../Acquired Podcast Questions.csv', 'r') as reader:
    writer = csv.writer(file)
    csv_reader = csv.DictReader(reader)

    for datapoint in csv_reader:

        if datapoint_index >= 5000:
            quit(0)
        if datapoint_index%10==0:
            print('datapoint index: '+str(datapoint_index))
        if(datapoint_index < starting_datapoint_index):
            datapoint_index+=1
            continue

        question = datapoint['question']

        answer = datapoint['answer']
        docs = retriever.retrieve(question)
        context_string = ''
        source_index = 1
        for doc in docs:
            if len(context_string) <= 10000: #max 10k context chars
                context_string += f'\n\n----------\n\nSource #{source_index}: \n"'
                context_string+=doc.text+'"'
                source_index+=1


        writer.writerow([question, answer, context_string])


        
        datapoint_index+=1



