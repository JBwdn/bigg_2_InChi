"""
Collect InChi string per metabolite based on its bigg identifier.
J.Bowden 05/20
"""


import pandas as pd  # fast csv reading and writing
import tqdm  # tidy progress bars
import libchebipy  # ChEBI database API - Ref: Swainston2016

from requests import get  # send html get requests to BIGG
import json  # parse json format queries from BIGG


INPUT_CSV_PATH = "example.csv"
OUTPUT_CSV_PATH = "example_out.csv"

BIGG_API_URL = "http://bigg.ucsd.edu/api/v2/universal/metabolites/"


# Parse .csv format metabolite data:
print(f"Loading {INPUT_CSV_PATH}...")
input_csv_df = pd.read_csv(INPUT_CSV_PATH)
bigg_id_list = list(input_csv_df["bigg.id"])


# Query BIGG api for json format data on each metabolite, create dict of {bigg.id : ChEBI id}...
chebi_id_dict = {}

print("Fetching ChEBI identifiers from BIGG...")
for bigg_id in tqdm.tqdm(bigg_id_list):
    chebi_id = ""
    try:
        query = get(BIGG_API_URL + bigg_id)
        if query.status_code == 200:  # confirm status_code
            query_json = json.loads(query.text)
            chebi_id = query_json["database_links"]["CHEBI"][0]["id"]
    except (ConnectionError, KeyError) as errors:
        pass

    chebi_id_dict[bigg_id] = chebi_id


# Query ChEBI database to collect InChI string..
inchi_str_list = []
fails_counter = 0

print("Fetching InChI strings from ChEBI...")
for key in tqdm.tqdm(chebi_id_dict.keys()):
    if chebi_id_dict[key] != "":
        chebi_entity = libchebipy.ChebiEntity(chebi_id_dict[key])
        inchi_str = chebi_entity.get_inchi()
        inchi_str_list.append(inchi_str)
    else:
        inchi_str_list.append("NaN")
        fails_counter += 1
print(f"Number of entries without found InChI strings: {fails_counter}.")


# Add data to df and save to new csv file:
print(f"Saving to {OUTPUT_CSV_PATH}...")
input_csv_df["InChI_string"] = inchi_str_list
input_csv_df.to_csv(OUTPUT_CSV_PATH, index=False)


if __name__ == "__main__":
    pass
