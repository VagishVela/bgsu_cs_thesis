import sys
import pubmed_parser as pp
import pandas as pd
import numpy as np
from csv import DictWriter
import time

def get_total_words_from_column(df_column):
    '''
    Input: df_column
    Output: total words in the column
    '''
    column_list = df_column.to_list()
    while ('' in column_list):
        column_list.remove('')
    return sum(list(map(lambda x: len(x.split()), column_list)))

print("Loading data...")

start_path_xml = time.process_time()

#path_xml = pp.list_xml_path('/users/PCS0221/c8fsfp4hp4wmsn4upmuq/ftp.ncbi.nlm.nih.gov/pubmed/baseline') # list all xml paths under directory
path_xml = pp.list_xml_path('data/raw') # list all xml paths under directory

print("Found {} xml files".format(len(path_xml)) + " in {:.2f} seconds".format(time.process_time() - start_path_xml))

print("Parsing data...")

for path in path_xml:
  start = time.process_time()
  pubmed_dict = pp.parse_medline_xml(path)
  df = pd.DataFrame(pubmed_dict)
  total = len(df)
  availableDf = df.replace(r'^\s*$', np.nan, regex=True).count().to_dict()
  availableDf["total words"] = get_total_words_from_column(df["abstract"])
  availableDf["path"] = path
  availableDf["total"] = total
  print(availableDf)

  with open('00_available_data.csv', 'a') as file_obj:
    dw_obj = DictWriter(file_obj, fieldnames=availableDf.keys())
    if file_obj.tell() == 0:
      dw_obj.writeheader()
    dw_obj.writerow(availableDf)

    file_obj.close()

  print("Parsed {} in {:.2f} seconds".format(path, time.process_time() - start))
  print("Estimated total time" + " {:.2f} seconds".format((time.process_time() - start_path_xml) * len(path_xml)))

sys.exit(0)
