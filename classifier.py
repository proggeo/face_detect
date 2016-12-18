import json

import cognitive_face as CF
import os
from time import sleep
import pandas as pd

KEY = ''  # Replace with a valid Subscription Key here.
CF.Key.set(KEY)

data = json.load(open('result.json'))

GROUP_ID = data['group_id']

files = [x[2] for x in os.walk('./test')]
files = files[0]

print files

results = {}

for file in files:
    if file.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
        imgfile = open('./test/' + file)
        print imgfile
        try:
            results[file] = {}
            faces_detected = CF.face.detect(imgfile)
            face_ids = []
            for face in faces_detected:
                face_ids.append(face['faceId'])
            sleep(5)
            if len(face_ids) == 0:
                continue
            faces_identified = CF.face.identify(face_ids, GROUP_ID)
            print faces_identified
            for face in faces_identified:
                face_id = face['faceId']
                if len(face['candidates']) == 0:
                    continue
                person_id = face['candidates'][0]['personId']
                confidence = face['candidates'][0]['confidence']
                person_name = "Not Found"
                for person in data['persons']:
                    if data['persons'][person]['person_id'] == person_id:
                        person_name = person
                results[file][person_name] = 'Found (' + str(confidence) + ')'
            sleep(5)
        except CF.util.CognitiveFaceException:
            pass

print results

with open('classification_result.json', 'w') as outfile:
    json.dump(results, outfile)

df = pd.DataFrame(results)
print df
df.to_csv('classification_result.csv')