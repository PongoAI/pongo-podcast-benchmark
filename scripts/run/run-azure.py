from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
import time
import csv

index_name = 'YOUR_AZURE_INDEX'
endpoint_name = 'YOUR_ENDPOINT_NAME'
key = 'YOUR_AZURE_KEY'
search_client = SearchClient(endpoint_name, index_name, AzureKeyCredential(key))



file_exists = False
try:
    with open('../results/azure-benchmark-results.csv', 'r') as file:
        file_exists = True
except FileNotFoundError:
    pass

if not file_exists:
    with open('../results/azure-benchmark-results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["question", "true_answer", 'context'])

vectorized_questions = []
starting_datapoint_index = 0
datapoint_index = starting_datapoint_index #long-running task so enable stopping and starting partway through

# try:
with open('.../results/azure-benchmark-results.csv', 'a', newline='') as file, \
        open('../../Acquired Podcast Questions.csv', 'r') as reader:
    writer = csv.writer(file)
    csv_reader = csv.DictReader(reader)

    for datapoint in csv_reader:
        print('a')
        if datapoint_index >= 5000:
            quit(0)
        if datapoint_index%10==0:
            print('datapoint index: '+str(datapoint_index))

        question = datapoint['question']
        answer = datapoint['answer']

        docs = search_client.search(question)
        
        context_string = ''
        source_index = 1
             
        for doc in docs:
            if len(context_string) <= 12000: #max 10k context chars
                context_string += f'\n\n----------\n\nSource #{source_index}: \n"'
                context_string+=doc['content']+'"'
                source_index+=1
            if(source_index >= 10):
                break

        openai_query_string = f'Please use ONLY the sources at the bottom of this prompt to give a short, concise answer the follwoing question.\n\nQuestion: "{question}"{context_string}'



        writer.writerow([question, answer, openai_query_string])


        
        datapoint_index+=1


# except:
#     print('failed at: '+str(datapoint_index))



