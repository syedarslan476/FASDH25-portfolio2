import pandas as pd
import plotly.express as px

# load regex counts and gazetteer
counts = pd.read_csv("../scripts/regex_counts.tsv", sep="\t")
coords = pd.read_csv("../gazetteers/geonames_gaza_selection.tsv", sep="\t")

# Rename 'asciiname' to 'placename' in the coords DataFrame to match counts
#(Help from ChatGpt- conversation 02)
coords.rename(columns={'asciiname': 'placename'}, inplace=True)

# Merge data on 'placename'
data = pd.merge(counts, coords, on="placename")

# Create animated map
fig = px.scatter_map(
    data,
    lat="latitude",  # This is latitude for location.
    lon="longitude",  # This is longitude for location
    hover_name="placename",  # Display the place name when hovering
    size="count",            # Size of the point based on count 
    animation_frame="month",   # animate the map by month
    projection_type="natural earth", # Use of natural earth projection for the map
    title="Regex-extracted Place Names by Month"   # Title of the map
)

# Show interactive map
fig.show()

# Save to HTML and PNG
fig.write_html("regex_map.html")
fig.write_image("regex_map.png")
