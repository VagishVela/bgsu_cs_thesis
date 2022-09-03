import sys
import pubmed_parser as pp
import nltk
import json
import os.path

def get_bag_of_words_from_corpus (corpus, stop_words=[], stemming=False):
    sno_stemmer = nltk.stem.SnowballStemmer('english')
    bag_of_words = []
    for doc in corpus:
        docWords = []
        for term in nltk.word_tokenize(doc['abstract']):
            if term.lower() not in stop_words:
                if stemming:
                    docWords.append(sno_stemmer.stem(term))
                else:
                    docWords.append(term)
        bag_of_words.append(
            {
                'nlm_unique_id': doc['nlm_unique_id'],
                'bag_of_words': docWords
            }
        )
    return bag_of_words

def get_all_terms_from_corpus(bag_of_words_corpus):
    all_terms = set()

    for doc in bag_of_words_corpus:
        all_terms.update(doc['bag_of_words'])
    return list(all_terms)

# This conversion to a dataframe causes some issues as the array isn't going through properly.
def write_dict_to_json(dict, file_name):
    f = open('/fs/scratch/PCS0221/data/processed/abstract_bag_of_words/' + file_name + '.json', "w")
    json.dump(dict, f)
    f.close()

#nltk.download('punkt')

print("Loading data...")

path_xml = pp.list_xml_path('/users/PCS0221/c8fsfp4hp4wmsn4upmuq/ftp.ncbi.nlm.nih.gov/pubmed/baseline') # list all xml paths under directory

print("Found {} xml files".format(len(path_xml)))

print("Parsing data...")

for path in path_xml:
  pubmed_dict = pp.parse_medline_xml(path)
  if os.path.isfile('/fs/scratch/PCS0221/data/processed/abstract_bag_of_words/' + path.split('/')[-1].split('.')[0] + '.json'):
    print('Skipped: ' + path.split('/')[-1].split('.')[0])
  else:
    write_dict_to_json(get_bag_of_words_from_corpus(pubmed_dict), path.split('/')[-1].split('.')[0])
    print('Completed: ' + path.split('/')[-1].split('.')[0])

sys.exit(0)
