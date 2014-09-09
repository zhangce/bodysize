#! /usr/bin/env python
import json, re, sys, os

BASE_FOLDER = os.path.split(os.path.realpath(__file__))[0]

dict_fossils = {} # This dictionary contains a map from taxon name to rank
dict_species_lastword = {} # This dictionary contains a set of valid species name

for l in open(BASE_FOLDER + '/../dict/treatise_measurements.txt').read().splitlines():
  ss = l.split('\t')
  a = ss[1].split(' ')[0]
  dict_fossils[a.lower()] = 'genus'
  if len(ss[1].split(' ')) == 2:
    dict_species_lastword[ss[1].split(' ')[1]] = 1

for l in open(BASE_FOLDER + '/../dict/paleodb_taxons.tsv'):
  try:
    (rawname, rank) = l.rstrip().split('\t')

    ss = rawname.split(' ')
    if len(ss) == 1:
      dict_fossils[ss[0].lower()] = rank
    elif len(ss) == 2:
      if '(' not in rawname:
        dict_fossils[rawname.lower()] = rank
        if len(ss[0]) > 4:
          dict_fossils[ss[0].lower()] = "genus"
      else:
        for s in ss:
          if '(' in s:
            s = s.replace('(', '').replace(')', '')
          if 'species' in rank and ' ' not in s: continue
          dict_fossils[s.lower()] = rank
    elif len(ss) == 3:
      if '(' not in rawname:
        dict_fossils[name.lower()] = rank
      elif '(' in ss[1] and '(' not in ss[2] and '(' not in ss[0]:
        dict_fossils[(ss[0]+" "+ss[2]).lower()] = rank
        dict_fossils[(ss[1].replace('(', '').replace(')', '')+" "+ss[2]).lower()] = rank

    if 'species' in rank and len(ss) > 1 and len(ss[-1]) > 2:
      dict_species_lastword[ss[-1].lower()] = 1
  
  except:
    continue

# For each input tuple
cache = {} # the cache of (nearst) genus
for row in sys.stdin:
  sent = json.loads(row)
  docid = sent["sentence.docid"]
  sentid = sent["sentence.sentid"]
  words = sent["sentence.words"]

  prevword = "" # The previous word in the sentence when enumerating words
  id = 1 # Curernt word ID while enumerating words
  for w in words: ## For each word
    w2 = re.sub('[^a-zA-Z]', '', w) # remove non english words (most OCR errors)
    if w2 != '' and w2.lower() in dict_fossils and dict_fossils[w2.lower()] == 'genus': # if this word is a genus
      cache[w2.lower()[0]] = w2.lower() # udpate the cache of (nearst) genus (P -> Pxxxxxxx)

    egenus = "" # result of searching for taxons. It will be != "" if we find a genus
    if w.lower() in dict_species_lastword: # if the current word is a valid species name
      if prevword.lower() in dict_fossils and prevword != "": # If the previous word is a higher-rank taxon
        egenus = prevword + ' ' + w
        egenus = re.sub('[^a-zA-Z ]', '' , egenus.encode('ascii', 'ignore'))
      elif prevword != "": # Check cases for abbrv. 
        prev2 = re.sub('[^a-zA-Z0-9\.]', '', prevword)
        if re.search('^[A-Z]\.?$', prev2):
          if prev2[0].lower() in cache:
            egenus = cache[prev2[0].lower()] + ' ' + w.lower()
            egenus = re.sub('[^a-zA-Z ]', '' , egenus.encode('ascii', 'ignore'))

    if egenus != "": # If we found a genus, output a mention
      mid = "TAXON_" + sentid + "_%d_%d" % (id-1, id)
      print json.dumps({"docid":docid, "mid":mid, "word":egenus, "type":"TAXON"})

    prevword = w
    id = id + 1





