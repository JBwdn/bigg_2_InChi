# bigg_2_InChi
Fetch InChi strings from a metabolite's BiGG identifier 

Method: 
- Query BiGG API to get ChEBI identifiers
- Fetch InChi string from ChEBI database 
- Save strings as new column in input csv

Requirements:
- pandas
- tqdm
- libchebipy (pip install libChEBIpy)

Usage: set input/output csv paths in "main.py" and execute script
