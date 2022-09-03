import sys
import nltk
import json
import glob

def get_all_terms_from_corpus(bag_of_words_corpus):
    all_terms = set()

    for doc in bag_of_words_corpus:
        all_terms.update(doc['bag_of_words'])
    return list(all_terms)

def write_dict_to_json(dict, file_name):
    f = open('/fs/scratch/PCS0221/data/processed/all_terms/' + file_name + '.json', "w")
    json.dump(dict, f)
    f.close()

def read_dict_from_json(path):
    with open(path) as json_file:
        return json.load(json_file)

def get_file_name_from_path(path):
    return path.split('/')[-1].split('.')[0]

nltk.download('punkt')

print("Loading data...")

paths_json = glob.glob('/fs/scratch/PCS0221/data/processed/abstract_bag_of_words/*') # list all xml paths under directory

print("Found {} json files".format(len(paths_json)))

print("Parsing data...")

for path in paths_json:
  write_dict_to_json(get_all_terms_from_corpus(read_dict_from_json(path)), get_file_name_from_path(path))

sys.exit(0)
