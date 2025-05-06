import pandas as pd
import plotly.express as px

# load regex counts and gazetteer
counts = pd.read_csv("../scripts/regex_counts.tsv", sep="\t")
coords = pd.read_csv("../gazetteers/geonames_gaza_selection.tsv", sep="\t")

# Rename 'asciiname' to 'placename' in the coords DataFrame to match counts
#(Help from ChatGpt- conversation 01)
coords.rename(columns={'asciiname': 'placename'}, inplace=True)

# Merge data on 'placename'
data = pd.merge(counts, coords, on="placename")

# Create animated map
fig = px.scatter_geo(
    data,
    lat="latitude",
    lon="longitude",
    hover_name="placename",
    size="count",
    animation_frame="month",
    projection="natural earth",
    title="Regex-extracted Place Names by Month"
)

# Show interactive map
fig.show()

# Save to HTML and PNG
fig.write_html("regex_map.html")
fig.write_image("regex_map.png")
