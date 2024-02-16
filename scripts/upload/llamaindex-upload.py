from llama_index import SimpleDirectoryReader
from llama_index.vector_stores import PineconeVectorStore
from llama_index.node_parser import SentenceSplitter
from llama_index.schema import TextNode
from llama_index.extractors import (
    QuestionsAnsweredExtractor,
    TitleExtractor,
)

import pinecone
from llama_index.embeddings import OpenAIEmbedding


embed_model = OpenAIEmbedding(model="text-embedding-3-large", api_key='YOUR_OAI_KEY', dimensions=3072)

pinecone_api_key = 'YOUR_PINECONE_KEY'
pinecone_environment = 'us-east1-gcp'
pinecone.init(api_key=pinecone_api_key, environment=pinecone_environment)

index_name = 'oai-large-podcast'
pinecone.create_index(index_name, dimension=3072, metric="euclidean", pod_type="p1" )

pinecone_index = pinecone.Index(index_name)



vector_store = PineconeVectorStore(pinecone_index=pinecone_index)

reader = SimpleDirectoryReader("../../acquired_transcripts")

text_splitter = SentenceSplitter(
    chunk_size=280,
    chunk_overlap=50,
    separator=" ",
)

nodes = []

for docs in reader.iter_data():
    cur_doc = docs[0]
    cur_text_chunks = text_splitter.split_text(cur_doc.text)

    for text_chunk in cur_text_chunks:
        cur_node = TextNode(text=text_chunk)
        cur_node.metadata['file_name'] = cur_doc.metadata['file_name']
        nodes.append(cur_node)
        


print('embedding')

for node in nodes:
    node_embedding = embed_model.get_text_embedding(
        node.get_content(metadata_mode="all")
    )
    node.embedding = node_embedding

vector_store.add(nodes)