import uuid
import requests
import time
import pongo

PONGO_SECRET='YOUR_PONGO_SECRET' 
pongo_client = pongo.PongoClient(PONGO_SECRET)
starting_index = 0
datapoint_index = starting_index


#Creates a new sub org.  Save the ID so you can use it when running later
sub_org_id = pongo_client.create_sub_org('Podcast Sub Org').json()['sub_org_id']
print(f"uploading to Pongo sub org with ID {sub_org_id}. Save this for searching later")
try:
    import os
    for filename in os.listdir("../../acquired_transcripts"):
        if filename.endswith(".txt"):
            with open(os.path.join("../../acquired_transcripts", filename), 'r') as file:
                data = file.read()
                title = filename[:-4]

                pongo_client.upload(data=data, metadata={'data_group': 'podcast', 'parent_id': title, 'source': title}, sub_org_id=sub_org_id)
                print(f'Uploaded {title}')

except RuntimeError as e:
    print(e)
    print('failed at '+str(datapoint_index))
    quit(0)

