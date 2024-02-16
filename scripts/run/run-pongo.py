import csv
import requests
import time 
import pongo

sub_org_id='' #Paste sub-org-id from previous step
pongo_client = pongo.PongoClient('YOUR_PONGO_SECRET_KEY')

#If you don't have the sub-org-id, use this snippet to find it
if sub_org_id == '':
    print(pongo_client.get_sub_orgs().json()) 
    quit(0)

file_exists = False
try:
    with open('../results/pongo-acquired-benchmark-results.csv', 'r') as file:
        file_exists = True
except FileNotFoundError:
    pass

if not file_exists:
    with open('../results/pongo-acquired-benchmark-results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["question", 'answer', 'context'])

vectorized_questions = []
starting_datapoint_index = 0
datapoint_index = starting_datapoint_index #long-running task so enable stopping and starting partway through

# try:
with open('../results/pongo-acquired-benchmark-results.csv', 'a', newline='') as file, \
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

        has_retried = False
        while True:

            response = pongo_client.search(query=question, sub_org_id=sub_org_id)

            print(response.ok)

            if(response.ok):
                break
            elif has_retried:
                raise RuntimeError('Failed to complete pongo query, please try again later.')
            else:
                time.sleep(1)
                has_retried = True

        docs =  response.json()

        context_string = ''
        source_index = 1
        for doc in docs:
            if len(context_string) <= 10000: #max 10k context chars
                context_string += f'\n\n----------\n\nSource #{source_index}: \n"'
                context_string+=doc['text']+'"'
                source_index+=1


        writer.writerow([question, answer, context_string])


        
        datapoint_index+=1



