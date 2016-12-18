import json

import cognitive_face as CF
import os
from time import sleep

KEY = ''  # Replace with a valid Subscription Key in credentials.json.
with open('credentials.json') as outfile:
    KEY = json.load(outfile)
CF.Key.set(KEY)

GROUP_ID = '2'
CF.person_group.create(GROUP_ID)

a = os.walk('.')
folders = [x[0] for x in a]
persons = {}
for folder in folders:
    if len(folder) > 2 and folder[2] != '.' and not (folder.startswith('./test') or folder.startswith('./cognitive_face')):
        print folder
        persons[folder[2:]] = {}

for person in persons:
    persons[person]['img'] = []
    files = [x[2] for x in os.walk('./' + person)]
    files = files[0]
    for file in files:
        if file.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
            persons[person]['img'].append('./' + person + '/' + file)

for person in persons:
    persons[person]['person_id'] = CF.person.create(GROUP_ID, person)['personId']
    sleep(5)
    for img in persons[person]['img']:
        print img
        imgfile = open(img)
        try:
            CF.person.add_face(imgfile, GROUP_ID, persons[person]['person_id'])
        except CF.util.CognitiveFaceException:
            pass
        sleep(5)

CF.person_group.train(GROUP_ID)

sleep(10)

trained = False

while not trained:
    result = CF.person_group.get_status(GROUP_ID)
    trained = result['status'] == 'succeeded'
    if not trained:
        sleep(10)

print 'Training completed'

result = {'group_id': GROUP_ID, 'persons': persons}

with open('result.json','w') as outfile:
    json.dump(result,outfile)