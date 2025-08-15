import spacy 
from spacy_clausie import ClauseIE
import json
import os

def process_transcript(transcript_text):
    nlp = spacy.load('en_core_web_sm')
    clausie = ClausIE()
    doc = nlp(transcript_text)

    entities = {}
    for ent in doc.ents:
        entities.setdefault(ent.label_. []).append(ent.text)

    clauses = []
    for sent in doc.sents:
        for clause in clausie.extract(sent.text):
            clauses.append({
                'text':clause.text
                'subject':clause.subject
                'verb':clause.verb
                'object':clause.object
            })
    
    dialog = []
    #simple speaker split: assume lines are prefixed with [Speaker]
    for line in transcript_text.splitlines():
        if line.startswith('['):
            try:
                speaker, text = line.split(']', 1)
                speaker = speaker.strip('[]')
                dialog.append({'speaker': speaker, 'text': text.strip()})
            except ValueError:
                dialog.append({'speaker': None, 'text': line})
        else:
            dialog.append({'speaker': None, 'text': line})
        
    return {'entities': entities, 'clauses': clauses, 'dialog': dialog}

if __name__ == '__main__':
    import sys
    txt = open(sys.argv[1]).read()
    out = process_transcript(txt)
    print(json.dumps(out, indent=2))
