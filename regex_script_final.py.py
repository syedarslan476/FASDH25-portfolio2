import re # import the regular expressions to help me match places in article text. 
import os # import the os module.  
import pandas as pd # import the pandas for working with the tabular data like TSV files.

# fix this function!

def write_tsv(rows, column_list, path):
   
    # turn the dictionary into a list of (key, value) tuples (this is correct):
    # create a dataframe from the items list (this is correct):
    #convert the data (list of rows) into a DataFrame with specified column names
    df = pd.DataFrame(rows, columns=column_list)
    # write the dataframe to tsv:
    # save the DataFrame to a .tsv file without the index column
    df.to_csv(path, sep="\t", index=False)



# define which folder to use:
# NB: these are different articles than in the previous weeks
folder = "articles"  # defining the folder that contains the articles. these are different from the articles that were used previously in class.

# define the patterns we want to search:
# Help from Chatgpt Conversation 01.
# load the gazetteer from the tsv file:
path = "gazetteers/geonames_gaza_selection.tsv" # load the gazatteers file contaning place names and alternate spellings
with open(path, encoding="utf-8") as file:
    data = file.read()

# build a dictionary of patterns from the place names in the first column: 
patterns = {} # start with empty dictionary to store place names and their regex patterns and counts
rows = data.split("\n") # splitting of file data into rows (each row representing a place entry)
for row in rows[1:]: # process each row except the header
    columns = row.split("\t")

    if len(columns) < 6: # checking for enough columns to inlcude alternate names (in column 6 or beyond)
        continue

    asciiname = columns[0]. strip()
    if not asciiname: # only proceed if the main name is not empty
        continue 
        

    
    name_variants = [re.escape(asciiname)] #start a list of name variants with the main name

    alternate_names = columns[5].strip() #extract alternate names from column and clean up using .strip() 
    if alternate_names:
        # in case of multiple alternate names split them by comma
        alternate_list =alternate_names.split(",")
        for alternate in alternate_list:
            alternate = alternate.strip() # clean each name using .strip() to remove extra spaces or newline characters
            if alternate:
                name_variants.append(re.escape(alternate)) 
                
   # join all name variants into a regex pattern using |
   # this will then match any one of the names in the list
    regex_pattern = "|".join(name_variants)
    patterns[asciiname]= {"pattern": regex_pattern, "count": 0} # update the dictionary entry to include the complete regex pattern
                


mentions_per_month = {}        
#War time in Gaza  ###(Help from Chatgpt Conversation:02)
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
        
        if count>0:   # (chatgpt help conversation 03 and 04)
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
