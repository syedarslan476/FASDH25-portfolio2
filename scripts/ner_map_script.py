#importing the libraries
import pandas as pd
import plotly.express as px

#  Loading the tsv data into data frame
ner_counts = pd.read_csv("ner_counts.tsv", sep="\t")
gazetteer = pd.read_csv("NER_gazetteer.tsv", sep="\t")

# Renaming columns in both dataframes to have consistent names for easier merging later taking help from chatgpt (conversation 4) and slides
ner_counts.rename(columns={"Place": "placename", "Count": "frequency"}, inplace=True)
gazetteer.rename(columns={"Name": "placename", "Latitude": "latitude", "Longitude": "longitude"}, inplace=True)

# Merge the NER counts with the gazetteer data using the common 'placename'
merged = pd.merge(ner_counts, gazetteer, on="placename")

# Ploting the placename on map
fig = px.scatter_geo(
    merged,
    lat="latitude",
    lon="longitude",
    hover_name="placename",  # this show place name when mouse goes over the point
    size="frequency",
    color="frequency",
    size_max=20,
    opacity=0.6,                #Took help from chatgpt(Conversation 4) for better improvements in map
    title="NER Place Name Frequencies - January 2024",
    projection="natural earth",
    color_continuous_scale="Viridis"
)

fig.update_layout(
    geo=dict(showland=True, landcolor="LightGray"), #Took help from chatgpt(Conversation4) for color addition
    margin={"r":0,"t":50,"l":0,"b":0}               #Adjust the margin around the map
)

fig.write_html("ner_map.html") # Save the map as a HTML file
fig.write_image("ner_map.png") # Save the map as a PNG image

# Display the map
fig.show()
