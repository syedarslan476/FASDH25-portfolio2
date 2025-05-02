import re
import os
import pandas as pd

# fix this function!

def write_tsv(rows, column_list, path):
   
    # turn the dictionary into a list of (key, value) tuples (this is correct):
    # create a dataframe from the items list (this is correct):
    df = pd.DataFrame(rows, columns=column_list)
    # write the dataframe to tsv:
    df.to_csv(path, sep="\t", index=False)



# define which folder to use:
# NB: these are different articles than in the previous weeks
folder = "articles"  

# define the patterns we want to search:

# load the gazetteer from the tsv file:
path = "gazetteers/geonames_gaza_selection.tsv"
with open(path, encoding="utf-8") as file:
    data = file.read()

# build a dictionary of patterns from the place names in the first column: 
patterns = {}
rows = data.split("\n")
for row in rows[1:]:
    columns = row.split("\t")
    asciiname = columns[0]
    if asciiname:
        patterns[asciiname] = {"pattern": re.escape(asciiname), "count": 0}
    if len(columns) < 6:
        continue
    name_variants = [asciiname]
    alternate_names = columns[5].strip()
    
    if alternate_names:
        
        alternate_list =alternate_names.split(",")
        for alternate in alternate_list:
            alternate = alternate.strip()
            if alternate:
                name_variants.append(alternate)
                
    regex_pattern = "|".join(name_variants)
    patterns[asciiname]= {"pattern": regex_pattern, "count": 0}
                


mentions_per_month = {}        
#War time in Gaza  
war_start_date = "2023-10-07"

# count the number of times each pattern is found in the entire folder:
for filename in os.listdir(folder):
    date_str = filename.split("_")[0]
    if date_str < war_start_date:
        continue
    
    

# build the file path:
    file_path = os.path.join(folder, filename)        
    #print(f"The path to the article is: {file_path}")
    # load the article (text file) into Python:
    with open(file_path, encoding="utf-8") as file:
        text = file.read()
        

    # find all the occurences of the patterns in the text:
    for place in patterns:
        pattern = patterns[place]["pattern"]
        matches = re.findall(pattern, text, re.IGNORECASE)
        count = len(matches)
            # add the number of times it was found to the total frequency:
        patterns[place]["count"] += count

        month_str = date_str[:7]

        if place not in mentions_per_month:
            mentions_per_month[place] = {}
        if month_str not in mentions_per_month[place]:
            mentions_per_month[place][month_str] = 0
        mentions_per_month[place][month_str] += count
          

# print the frequency of each pattern:
for place in mentions_per_month:
    print(f'"{place}": {{')
    month_list = list(mentions_per_month[place].keys())
    for month in month_list:
        count = mentions_per_month[place][month]
        if month != month_list[-1]:
            print(f'    "{month}": {count},')
        else:
            print(f'    "{month}": {count}')
    print("},")

rows = []
for place in mentions_per_month:
    for month in mentions_per_month[place]:
        count = mentions_per_month[place][month]
        rows.append((place, month, count))
        
write_tsv(rows, ["placename","month", "count"], "regex_counts.tsv")
